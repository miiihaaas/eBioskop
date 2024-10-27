# ebioskop/cinemas/utils/pdf_generator.py

from fpdf import FPDF
import locale
from datetime import datetime
import os

# Definišemo putanje do fontova
current_file_path = os.path.abspath(__file__)
project_folder = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))
font_path = os.path.join(project_folder, 'static', 'fonts', 'DejaVuSansCondensed.ttf')
font_path_B = os.path.join(project_folder, 'static', 'fonts', 'DejaVuSansCondensed-Bold.ttf')

class CinemaPDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font('DejaVuSansCondensed', '', font_path, uni=True)
        self.add_font('DejaVuSansCondensed', 'B', font_path_B, uni=True)
    
    def header(self):
        self.set_font('DejaVuSansCondensed', 'B', 15)
        self.cell(80)
        self.cell(30, 10, 'Lična karta bioskopa', 0, 0, 'C')
        self.ln(20)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVuSansCondensed', '', 8)
        self.cell(0, 10, f'Stranica {self.page_no()}/{{nb}}', 0, 0, 'C')
        
    def chapter_title(self, title):
        self.set_font('DejaVuSansCondensed', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)
        
    def chapter_body(self, data_dict):
        for key, value in data_dict.items():
            if value is not None and value != '':
                self.set_font('DejaVuSansCondensed', 'B', 11)
                self.cell(60, 6, f"{key}:", 0, 0)
                self.set_font('DejaVuSansCondensed', '', 11)
                
                # Provera da li je value bool
                if isinstance(value, bool):
                    value = "Da" if value else "Ne"
                
                # Ako je value string i duži od 50 karaktera, prelomi ga
                if isinstance(value, str) and len(value) > 50:
                    self.multi_cell(0, 6, str(value))
                else:
                    self.cell(0, 6, str(value), 0, 1)
        self.ln(4)

def generate_cinema_pdf(cinema):
    """
    Generiše PDF dokument za dati bioskop
    
    Args:
        cinema: Cinema model instance
        
    Returns:
        bytes: PDF dokument kao bytes objekat
    """
    try:
        # Postavimo locale na srpski
        try:
            locale.setlocale(locale.LC_ALL, 'sr_RS.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_ALL, '')
        
        # Kreiramo PDF
        pdf = CinemaPDF()
        pdf.alias_nb_pages()
        pdf.add_page()
        
        # Podaci o pravnom licu
        pdf.chapter_title('Podaci o pravnom licu')
        legal_data = {
            'Naziv': cinema.name,
            'Zemlja': cinema.country,
            'Adresa': cinema.address,
            'Poštanski broj': cinema.postal_code,
            'Mesto': cinema.city,
            'Opština': cinema.municipality,
            'Email': cinema.email,
            'Telefon': cinema.phone,
            'PIB': cinema.pib,
            'Matični broj': cinema.mb,
            'Website': cinema.website,
            'Član MKPS': cinema.is_member_mkps,
            'Član EC': cinema.is_member_ec
        }
        pdf.chapter_body(legal_data)
        
        # Podaci o zastupnicima
        if cinema.representatives:
            pdf.chapter_title('Podaci o zastupnicima')
            for rep in cinema.representatives:
                rep_data = {
                    'Ime': rep.first_name,
                    'Prezime': rep.last_name,
                    'Pozicija': rep.position,
                    'Email': rep.email,
                    'Telefon': rep.phone
                }
                pdf.chapter_body(rep_data)
                
        # Podaci o bioskopu
        if cinema.properties:
            pdf.chapter_title('Podaci o bioskopu')
            cinema_data = {
                'Lokacija': cinema.properties.location,
                'Broj stanovnika (grad)': f"{cinema.properties.city_population:,}",
                'Broj stanovnika (sa okolinom)': f"{cinema.properties.surrounding_population:,}",
                'E-karte': cinema.properties.has_e_ticket_system,
                'Sistem e-karata': cinema.properties.e_ticket_system,
                'Metode promocije': cinema.properties.promotion_methods,
                'Metode programiranja': cinema.properties.programming_methods,
                'Takođe distributer': cinema.properties.is_distributor
            }
            pdf.chapter_body(cinema_data)
            
            # Podaci o salama
            if cinema.properties.halls:
                pdf.chapter_title('Podaci o salama')
                for hall in cinema.properties.halls:
                    hall_data = {
                        'Naziv sale': hall.hall_name,
                        'Kapacitet': hall.hall_capacity,
                        'Godina izgradnje': hall.year_built,
                        'Dimenzije': hall.dimensions,
                        'Udaljenost od ekrana': f"{hall.distance_to_screen} m",
                        'Klimatizacija': hall.has_air_conditioning,
                        'Grejanje': hall.has_heating,
                        'Zvučni sistem': hall.sound_system,
                        'Digitalizovana': hall.is_digitalized
                    }
                    if hall.is_digitalized:
                        hall_data.update({
                            'Projektor': f"{hall.projector_brand} {hall.projector_model}",
                            'Rezolucija': hall.projector_resolution,
                            'Lumeni': hall.projector_lumens,
                            '3D oprema': hall.has_3d_equipment
                        })
                    pdf.chapter_body(hall_data)
        
        # Vraćamo PDF kao bytes
        return bytes(pdf.output())  # Ovo je izmenjeni deo
        
    except Exception as e:
        raise Exception(f"Greška pri generisanju PDF-a: {str(e)}")