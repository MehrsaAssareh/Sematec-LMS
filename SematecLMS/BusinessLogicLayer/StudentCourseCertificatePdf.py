import math
import os
import re
from datetime import date, datetime
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError


class StudentCourseCertificatePdfGenerator:
    PAGE_SIZE = (1684, 1190)
    PDF_RESOLUTION = 144.0

    BLUE = '#174C99'
    DARK_BLUE = '#123C78'
    YELLOW = '#FFD528'
    GOLD = '#D8A852'
    LIGHT_GRAY = '#EEF1F3'
    MID_GRAY = '#D8DEE3'
    TEXT = '#191919'

    def create_pdf(self, certificate_data, output_path):
        if not output_path.lower().endswith('.pdf'):
            output_path = f'{output_path}.pdf'

        image = self.create_certificate_image(certificate_data)
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
        image.save(output_path, 'PDF', resolution=self.PDF_RESOLUTION)
        return output_path

    def create_certificate_image(self, data):
        width, height = self.PAGE_SIZE
        image = Image.new('RGB', self.PAGE_SIZE, 'white')
        draw = ImageDraw.Draw(image)

        self.draw_frame(draw, width, height)
        self.draw_left_panel(draw, image, data)
        self.draw_main_text(draw, data, width)
        self.draw_signatures(draw, width, height)
        return image

    def draw_frame(self, draw, width, height):
        draw.rectangle((14, 14, width - 15, height - 15), outline=self.BLUE, width=16)
        draw.rectangle((32, 32, width - 33, height - 33), outline=self.YELLOW, width=4)
        draw.rectangle((42, 42, width - 43, height - 43), outline=self.BLUE, width=3)

        bottom_top = height - 88
        draw.rectangle((42, bottom_top, width - 43, height - 43), fill=self.BLUE)
        self.draw_pattern(draw, (42, bottom_top, width - 43, height - 43), '#5D7DC0', step=42)

        for y in range(height - 198, bottom_top):
            shade = int(244 - ((y - (height - 198)) * 34 / 110))
            draw.line((42, y, width - 43, y), fill=(shade, shade, shade))
        draw.line((42, bottom_top, width - 43, bottom_top), fill=self.BLUE, width=2)

    def draw_left_panel(self, draw, image, data):
        x, y, panel_width = 128, 42, 320
        draw.rectangle((x, y, x + panel_width, y + 120), fill=self.BLUE)
        self.draw_pattern(draw, (x, y, x + panel_width, y + 120), '#7D98CE', step=52)

        strip_y = y + 120
        draw.rectangle((x, strip_y, x + panel_width, strip_y + 66), fill=self.YELLOW)
        self.draw_centered_text(
            draw,
            'SEMATEC Certified',
            x + panel_width / 2,
            strip_y + 15,
            self.font(34, bold=False),
            self.TEXT
        )

        panel_y = strip_y + 66
        panel_bottom = 870
        draw.rectangle((x, panel_y, x + panel_width, panel_bottom), fill=self.LIGHT_GRAY)
        self.draw_pattern(draw, (x, panel_y, x + panel_width, panel_bottom), '#FFFFFF', step=74)

        photo_box = (x + 55, panel_y + 60, x + panel_width - 55, panel_y + 330)
        self.draw_student_photo(draw, image, data.get('photo_content'), photo_box)
        self.draw_seal(draw, x + panel_width / 2, panel_y + 555)

    def draw_main_text(self, draw, data, width):
        content_left = 510
        content_right = width - 100
        center_x = (content_left + content_right) / 2

        self.draw_centered_text(draw, 'SEMATEC', center_x, 56, self.font(42, bold=True), self.BLUE)
        draw.line((center_x - 130, 118, center_x + 130, 118), fill='#8FA4D6', width=2)
        self.draw_centered_text(draw, 'Specialized IT Training Center', center_x, 126, self.font(22, bold=True),
                                self.BLUE)

        y = 188
        self.draw_centered_text(draw, 'Certificate of Completion', center_x, y, self.font(48, bold=True), self.TEXT)
        y += 88
        self.draw_centered_text(draw, 'This is to certify that', center_x, y, self.font(30, bold=True), self.TEXT)
        y += 88
        self.draw_centered_text(draw, data.get('student_name') or '', center_x, y, self.font(46, bold=True), self.TEXT)
        y += 88
        self.draw_centered_text(
            draw,
            'Has successfully completed the SEMATEC approved course:',
            center_x,
            y,
            self.font(31, bold=True),
            self.TEXT
        )

        y += 78
        course_lines = self.wrap_text(draw, data.get('course_name') or '', self.font(43, bold=True), 900)
        for line in course_lines[:2]:
            self.draw_centered_text(draw, line, center_x, y, self.font(43, bold=True), self.TEXT)
            y += 54

        y += 12
        details = self.get_course_details(data)
        for detail in details:
            self.draw_centered_text(draw, detail, center_x, y, self.font(25, bold=True), self.TEXT)
            y += 36

        y += 8
        certificate_number = data.get('certificate_number') or ''
        self.draw_centered_text(draw, f'Certificate No: {certificate_number}', center_x, y, self.font(24, bold=True),
                                self.BLUE)
        y += 34
        self.draw_centered_text(draw, f'Issued on {self.format_date(data.get("certificate_issue_date"))}', center_x, y,
                                self.font(24, bold=True), self.TEXT)

    def draw_signatures(self, draw, width, height):
        y = height - 350
        left_x = 720
        right_x = 1280

        self.draw_signature_mark(draw, left_x - 54, y - 40, scale=0.95)
        self.draw_signature_mark(draw, right_x - 54, y - 40, scale=0.82)

        draw.line((left_x - 170, y + 78, left_x + 170, y + 78), fill='#333333', width=2)
        draw.line((right_x - 170, y + 78, right_x + 170, y + 78), fill='#333333', width=2)

        self.draw_centered_text(draw, 'Training Department', left_x, y + 94, self.font(25, bold=True), self.TEXT)
        self.draw_centered_text(draw, 'Training Manager', left_x, y + 130, self.font(24), self.TEXT)
        self.draw_centered_text(draw, 'Sematec Management', right_x, y + 94, self.font(25, bold=True), self.TEXT)
        self.draw_centered_text(draw, 'CEO', right_x, y + 130, self.font(24), self.TEXT)

    def draw_student_photo(self, draw, image, photo_content, box):
        x1, y1, x2, y2 = [int(value) for value in box]
        draw.rounded_rectangle((x1 - 8, y1 - 8, x2 + 8, y2 + 8), radius=16, fill='white', outline=self.BLUE, width=4)

        try:
            photo = Image.open(BytesIO(photo_content))
            photo = ImageOps.exif_transpose(photo).convert('RGB')
        except (TypeError, UnidentifiedImageError, OSError):
            draw.rectangle((x1, y1, x2, y2), fill='#F8FAFB')
            self.draw_centered_text(draw, 'No Photo', (x1 + x2) / 2, (y1 + y2) / 2 - 14, self.font(24, bold=True),
                                    '#789')
            return

        photo = ImageOps.fit(photo, (x2 - x1, y2 - y1), method=Image.Resampling.LANCZOS, centering=(0.5, 0.45))
        mask = Image.new('L', photo.size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.rounded_rectangle((0, 0, photo.width, photo.height), radius=10, fill=255)
        image.paste(photo, (x1, y1), mask)

    def draw_seal(self, draw, center_x, center_y):
        center_x = int(center_x)
        center_y = int(center_y)
        points = []
        for index in range(40):
            angle = -math.pi / 2 + index * math.pi / 20
            radius = 118 if index % 2 == 0 else 99
            points.append((center_x + math.cos(angle) * radius, center_y + math.sin(angle) * radius))

        draw.polygon(points, fill=self.GOLD)
        draw.ellipse((center_x - 96, center_y - 96, center_x + 96, center_y + 96), fill='white', outline=self.GOLD,
                     width=6)
        draw.ellipse((center_x - 72, center_y - 72, center_x + 72, center_y + 72), outline=self.GOLD, width=3)
        self.draw_centered_text(draw, 'SEMATEC', center_x, center_y - 26, self.font(34, bold=True), self.GOLD)
        self.draw_centered_text(draw, 'CERTIFICATE', center_x, center_y + 17, self.font(18, bold=True), self.GOLD)
        self.draw_centered_text(draw, 'IT TRAINING', center_x, center_y + 48, self.font(16, bold=True), self.GOLD)

    def draw_signature_mark(self, draw, x, y, scale=1.0):
        points = [
            (x, y + 55), (x + 34 * scale, y + 4), (x + 60 * scale, y + 84),
            (x + 106 * scale, y + 34), (x + 150 * scale, y + 62),
            (x + 210 * scale, y + 20), (x + 285 * scale, y + 47)
        ]
        draw.line(points, fill='#101010', width=4, joint='curve')
        draw.arc((x - 28, y + 12, x + 80, y + 122), start=80, end=300, fill='#101010', width=3)

    def draw_pattern(self, draw, box, color, step=58):
        x1, y1, x2, y2 = [int(value) for value in box]
        for y in range(y1, y2, step):
            for x in range(x1, x2, step):
                center_x = min(x + step / 2, x2)
                center_y = min(y + step / 2, y2)
                right_x = min(x + step, x2)
                bottom_y = min(y + step, y2)

                draw.line((x, y, center_x, center_y), fill=color, width=1)
                draw.line((center_x, center_y, right_x, y), fill=color, width=1)
                draw.line((center_x, center_y, right_x, bottom_y), fill=color, width=1)
                draw.line((center_x, center_y, x, bottom_y), fill=color, width=1)

    def get_course_details(self, data):
        details = [f'Teacher: {data.get("teacher_name") or ""}']

        period = self.get_course_period(data)
        if period:
            details.append(period)

        term = data.get('term_number')
        score = data.get('score')
        duration = data.get('course_duration')
        term_score = []
        if term not in ('', None):
            term_score.append(f'Term {term}')
        if score not in ('', None):
            term_score.append(f'Final Score {score}')
        if duration not in ('', None):
            term_score.append(f'{duration} hours')
        if term_score:
            details.append(' - '.join(term_score))

        return details

    def get_course_period(self, data):
        start_date = data.get('actual_beginning_date') or data.get('planned_beginning_date')
        end_date = data.get('actual_finishing_date') or data.get('planned_finishing_date')
        if start_date and end_date:
            return f'{self.format_date(start_date)} - {self.format_date(end_date)}'
        if end_date:
            return f'Completed on {self.format_date(end_date)}'
        return None

    def wrap_text(self, draw, text, font, max_width):
        words = str(text).split()
        if not words:
            return ['']

        lines = []
        current = words[0]
        for word in words[1:]:
            candidate = f'{current} {word}'
            if self.text_width(draw, candidate, font) <= max_width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return lines

    def draw_centered_text(self, draw, text, center_x, y, font, fill):
        text = str(text)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        draw.text((center_x - text_width / 2, y), text, font=font, fill=fill)

    def text_width(self, draw, text, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        return bbox[2] - bbox[0]

    def font(self, size, bold=False):
        font_name = 'arialbd.ttf' if bold else 'arial.ttf'
        font_path = os.path.join(os.environ.get('WINDIR', r'C:\Windows'), 'Fonts', font_name)
        try:
            return ImageFont.truetype(font_path, size=size)
        except OSError:
            return ImageFont.load_default()

    def format_date(self, value):
        if value in ('', None):
            return ''
        if isinstance(value, datetime):
            value = value.date()
        if isinstance(value, date):
            return value.strftime('%d %B %Y')
        return str(value)


def build_default_certificate_filename(certificate_data):
    certificate_number = certificate_data.get('certificate_number') or 'certificate'
    student_name = certificate_data.get('student_name') or 'student'
    course_name = certificate_data.get('course_name') or 'course'
    filename = f'{certificate_number} - {student_name} - {course_name}.pdf'
    return sanitize_filename(filename)


def sanitize_filename(filename):
    filename = re.sub(r'[<>:"/\\\\|?*]', '-', filename)
    filename = re.sub(r'\s+', ' ', filename).strip()
    return filename[:180]
