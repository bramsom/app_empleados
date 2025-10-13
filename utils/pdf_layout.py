import os
import unicodedata
import tempfile
import uuid
from typing import Optional
from fpdf import FPDF
from PIL import Image
from datetime import datetime

def _safe_text(s: object) -> str:
    s = "" if s is None else str(s)
    s = s.replace("\u2013", "-").replace("\u2014", "-") \
         .replace("\u2018", "'").replace("\u2019", "'") \
         .replace("\u201c", '"').replace("\u201d", '"') \
         .replace("\u2026", "...").replace("\xa0", " ")
    # usar NFC para mantener caracteres acentuados precompuestos (evita crear combinantes)
    s = unicodedata.normalize("NFC", s)
    try:
        # forzar a latin-1 para compatibilidad con FPDF; caracteres no representables se reemplazan
        return s.encode("latin-1", "replace").decode("latin-1")
    except Exception:
        return s

def _ensure_image_rgb(path: str) -> Optional[str]:
    try:
        im = Image.open(path)
    except Exception:
        return None
    try:
        if im.mode not in ("RGB", "L"):
            im = im.convert("RGB")
        tmp = os.path.join(tempfile.gettempdir(), f"img_{uuid.uuid4().hex}.png")
        im.save(tmp, format="PNG")
        return tmp
    except Exception:
        return None

def _make_watermark(path: str, opacity: float = 0.18, target_width_mm: Optional[float]=None, pdf_obj=None) -> Optional[str]:
    try:
        im = Image.open(path).convert("RGBA")
    except Exception:
        return None
    try:
        alpha = int(255 * max(0.0, min(1.0, opacity)))
        if target_width_mm and pdf_obj:
            dpi = 150
            target_px = int(target_width_mm * dpi / 25.4)
            w_px, h_px = im.size
            scale = min(1.0, target_px / w_px)
            if scale < 1.0:
                new_w = int(w_px * scale)
                new_h = int(h_px * scale)
                im = im.resize((new_w, new_h), Image.ANTIALIAS)
        alpha_channel = im.split()[3].point(lambda p: int(p * (alpha / 255.0)))
        im.putalpha(alpha_channel)
        bg = Image.new("RGBA", im.size, (255, 255, 255, int(255 * (1 - opacity))))
        composed = Image.alpha_composite(bg, im)
        composed = composed.convert("RGB")
        tmp = os.path.join(tempfile.gettempdir(), f"wm_{uuid.uuid4().hex}.png")
        composed.save(tmp, format="PNG")
        return tmp
    except Exception:
        return None

class CertPDF(FPDF):
    def header(self):
        info = getattr(self, "header_info", {}) or {}
        entidad = _safe_text(info.get("entidad_nombre", ""))
        nit = _safe_text(info.get("nit", ""))
        contacto = _safe_text(info.get("contacto", ""))
        logo_left = info.get("logo_left")
        logo_right = info.get("logo_right")
        watermark = info.get("watermark")
        watermark_opacity = info.get("watermark_opacity", 0.18)
        watermark_scale = float(info.get("watermark_scale", 0.7))
        watermark_width_mm = info.get("watermark_width_mm", None)

        # opciones para separador decorativo
        separator_name = info.get("separator_name")               # nombre de archivo en carpeta imagenes
        separator_scale = float(info.get("separator_scale", 0.95))
        separator_width_mm = info.get("separator_width_mm", None)  # si se quiere ancho absoluto en mm
        separator_gap_mm = float(info.get("separator_gap_mm", 3))  # espacio entre línea y separador

        y_logo = 8
        logo_h_mm = 16
        left_w = right_w = 0

        if watermark and os.path.exists(watermark):
            util_width = (self.w - self.l_margin - self.r_margin)
            target_width_mm = util_width * max(0.0, min(1.0, float(watermark_scale)))
            wm_tmp = _make_watermark(watermark, opacity=watermark_opacity, target_width_mm=target_width_mm, pdf_obj=self)
            if wm_tmp and os.path.exists(wm_tmp):
                try:
                    w_mm = target_width_mm
                    try:
                        with Image.open(wm_tmp) as _im:
                            w_px, h_px = _im.size
                        aspect = w_px / h_px if h_px else 1
                        h_mm = w_mm / aspect
                    except Exception:
                        h_mm = w_mm * 0.5
                    x_w = self.l_margin + ((self.w - self.l_margin - self.r_margin) - w_mm) / 2
                    y_w = self.t_margin + 30
                    self.image(wm_tmp, x=x_w, y=y_w, w=w_mm, h=h_mm)
                finally:
                    try: os.unlink(wm_tmp)
                    except Exception: pass

        if logo_left and os.path.exists(logo_left):
            tmp_left = _ensure_image_rgb(logo_left)
            try:
                if tmp_left:
                    with Image.open(tmp_left) as im:
                        w_px, h_px = im.size
                    aspect = w_px / h_px if h_px else 1
                    left_w = logo_h_mm * aspect
                    self.image(tmp_left, x=self.l_margin, y=y_logo, w=left_w, h=logo_h_mm)
                else:
                    self.image(logo_left, x=self.l_margin, y=y_logo, h=logo_h_mm)
            except Exception:
                left_w = 0
            finally:
                if tmp_left and os.path.exists(tmp_left):
                    try: os.unlink(tmp_left)
                    except Exception: pass

        if logo_right and os.path.exists(logo_right):
            tmp_right = _ensure_image_rgb(logo_right)
            try:
                if tmp_right:
                    with Image.open(tmp_right) as im:
                        w_px, h_px = im.size
                    aspect = w_px / h_px if h_px else 1
                    right_w = logo_h_mm * aspect
                    x_right = self.w - self.r_margin - right_w
                    self.image(tmp_right, x=x_right, y=y_logo, w=right_w, h=logo_h_mm)
                else:
                    x_right = self.w - self.r_margin - (logo_h_mm * 1.0)
                    self.image(logo_right, x=x_right, y=y_logo, h=logo_h_mm)
            except Exception:
                right_w = 0
            finally:
                if tmp_right and os.path.exists(tmp_right):
                    try: os.unlink(tmp_right)
                    except Exception: pass

        self.set_xy(self.l_margin, y_logo)
        # usar fuente normal (no negrita) solo para el nombre de la entidad
        self.set_font("Arial", size=12)
        self.cell(0, 6, entidad, ln=1, align="C")

        self.set_font("Arial", size=8)
        self.multi_cell(0, 5, _safe_text("Licencia de Funcionamiento Preescolar, Primaria, Secundaría y \nMedia Vocacional No 11729 de Noviembre 2024"), align="C")
        self.cell(0, 5, _safe_text("DANE. 319548000692"), ln=1, align="C")

        if nit:
            self.set_font("Arial", size=8)
            self.cell(0, 4, nit, ln=1, align="C")

        # posición donde irá el separador (no dibujar la línea gris)
        y = self.get_y() + 2
        # si hay imagen de separador, dibujarla centrada justo debajo de la línea
        util_width = (self.w - self.l_margin - self.r_margin)
        if separator_name:
            # carpeta de imágenes (igual prepare_header_info)
            project_root = info.get("_project_root") or ""
            sep_path = None
            if project_root:
                sep_path = os.path.join(project_root, "images", separator_name)
            else:
                sep_path = separator_name  # permitir ruta absoluta/relativa directa

            if sep_path and os.path.exists(sep_path):
                tmp_sep = _ensure_image_rgb(sep_path)
                try:
                    if tmp_sep and os.path.exists(tmp_sep):
                        with Image.open(tmp_sep) as im:
                            w_px, h_px = im.size
                        aspect = w_px / h_px if h_px else 1
                        # calcular ancho objetivo: usa ancho absoluto si se da, sino fracción del ancho útil.
                        # limitada a 1.0 para respetar márgenes
                        if separator_width_mm:
                            w_mm = float(separator_width_mm)
                        else:
                            frac = max(0.0, min(1.0, float(separator_scale)))
                            w_mm = util_width * frac
                        h_mm = w_mm / aspect
                        x_sep = self.l_margin + (util_width - w_mm) / 2
                        y_sep = y + separator_gap_mm
                        try:
                             self.image(tmp_sep, x=x_sep, y=y_sep, w=w_mm, h=h_mm)
                        except Exception:
                             pass
                        # mover cursor debajo del separador
                        self.set_y(y_sep + h_mm + 2)
                finally:
                    try:
                        if tmp_sep and os.path.exists(tmp_sep):
                            os.unlink(tmp_sep)
                    except Exception:
                        pass
        else:
            self.ln(6)

    def footer(self):
        info = getattr(self, "header_info", {}) or {}
        # permitir usar el mismo separador del header o uno específico para el footer
        separator_name = info.get("footer_separator_name") or info.get("separator_name")
        separator_scale = float(info.get("separator_scale", 0.95))
        separator_width_mm = info.get("separator_width_mm", None)
        separator_gap_mm = float(info.get("separator_gap_mm", 3))

        # dibujar separador justo encima del área del pie (antes de posicionar el texto del footer)
        if separator_name:
            project_root = info.get("_project_root") or ""
            sep_path = os.path.join(project_root, "images", separator_name) if project_root else separator_name
            if sep_path and os.path.exists(sep_path):
                tmp_sep = _ensure_image_rgb(sep_path)
                try:
                    if tmp_sep and os.path.exists(tmp_sep):
                        with Image.open(tmp_sep) as im:
                            w_px, h_px = im.size
                        aspect = w_px / h_px if h_px else 1
                        util_width = (self.w - self.l_margin - self.r_margin)
                        if separator_width_mm:
                            w_mm = float(separator_width_mm)
                        else:
                            frac = max(0.0, min(1.0, float(separator_scale)))
                            w_mm = util_width * frac
                        h_mm = w_mm / aspect if aspect else 0
                        x_sep = self.l_margin + (util_width - w_mm) / 2
                        # calcular posición: el pie se coloca a 15mm del borde inferior (set_y(-15))
                        footer_top = self.h - 15
                        y_sep = footer_top - separator_gap_mm - h_mm
                        if y_sep < self.t_margin:
                            y_sep = self.t_margin
                        try:
                            self.image(tmp_sep, x=x_sep, y=y_sep, w=w_mm, h=h_mm)
                        except Exception:
                            pass
                finally:
                    try:
                        if tmp_sep and os.path.exists(tmp_sep):
                            os.unlink(tmp_sep)
                    except Exception:
                        pass

        # ahora dibujar el texto del pie como antes
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(100, 100, 100)
        footer_text = _safe_text("Web: www.ccp.com.co - Email: colecipi@hotmail.com - Teléfono: 3146233137 - Dirección: Cll. 2 No. 4-80 Barrio San Cayetano")
        self.cell(0, 6, footer_text, ln=0, align="C")

def prepare_header_info(project_root: str,
                        entidad_nombre: str,
                        nit: str,
                        contacto: str = "",
                        logo_left_name: str = "logo_institucional.png",
                        logo_right_name: str = "logo_fundacion.png",
                        watermark_name: Optional[str] = None,
                        watermark_opacity: float = 0.18,
                        watermark_scale: float = 0.7,
                        watermark_width_mm: Optional[float] = None,
                        separator_name: Optional[str] = None,
                        separator_scale: float = 1.0,
                        separator_width_mm: Optional[float] = None,
                        separator_gap_mm: float = 3.0,
                        logo_left_height_mm: Optional[float] = None,
                        logo_right_height_mm: Optional[float] = None):
    # carpeta de imágenes en el proyecto (usa "imagenes" como en tu proyecto)
    logo_dir = os.path.join(project_root, "images")
    logo_left = os.path.join(logo_dir, logo_left_name)
    logo_right = os.path.join(logo_dir, logo_right_name)
    watermark_path = os.path.join(logo_dir, watermark_name) if watermark_name else None
    separator_path = os.path.join(logo_dir, separator_name) if separator_name else None

    return {
        "entidad_nombre": entidad_nombre,
        "nit": nit,
        "contacto": contacto,
        "logo_left": logo_left if os.path.exists(logo_left) else None,
        "logo_right": logo_right if os.path.exists(logo_right) else None,
        "watermark": watermark_path if watermark_path and os.path.exists(watermark_path) else None,
        "watermark_opacity": watermark_opacity,
        "watermark_scale": watermark_scale,
        "watermark_width_mm": watermark_width_mm,
        "separator_name": separator_path if separator_path and os.path.exists(separator_path) else None,
        "separator_scale": separator_scale,
        "separator_width_mm": separator_width_mm,
        "separator_gap_mm": separator_gap_mm,
        "logo_left_height_mm": logo_left_height_mm,
        "logo_right_height_mm": logo_right_height_mm
    }