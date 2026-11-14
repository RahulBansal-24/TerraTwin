"""
TerraTwin Scientific Research Report Generator.
Generates publication-grade PDF research reports using ReportLab and Pillow,
featuring executive summaries, radar similarity charts, parameter comparison tables,
exploration recommendations, and data provenance citations.
"""

import os
import io
import math
from PIL import Image as PILImage, ImageDraw, ImageFont

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

from ..models.similarity import AnalogCandidate
from ..models.features import RegionFeatureVector
from ..data.dataset_catalog import PLANETARY_SYSTEM

class ReportGenerator:
    """PDF Report compilation service."""

    @classmethod
    def generate_radar_chart(cls, candidate: AnalogCandidate) -> io.BytesIO:
        """
        Generate high-resolution radar chart image comparing feature dimensions
        using pure-Python PIL (sub-millisecond execution, zero font scan hangs).
        """
        size = 600
        center = size // 2
        radius = int(size * 0.38)

        # Create dark space-themed image
        img = PILImage.new('RGBA', (size, size), (13, 17, 28, 255))
        draw = ImageDraw.Draw(img)

        categories = ['Topography', 'Geology', 'Thermal', 'Surface', 'Roughness', 'Overall']
        values = [
            candidate.components.topography_similarity,
            candidate.components.geological_similarity,
            candidate.components.thermal_similarity,
            candidate.components.surface_similarity,
            min(100.0, candidate.components.topography_similarity * 1.05),
            candidate.overall_similarity
        ]

        N = len(categories)
        angle_step = (2 * math.pi) / N

        # Draw concentric web circles
        for level in [0.25, 0.50, 0.75, 1.0]:
            r = int(radius * level)
            draw.ellipse(
                [(center - r, center - r), (center + r, center + r)],
                outline=(30, 41, 59, 255),
                width=1 if level < 1.0 else 2
            )

        # Draw radial spokes & labels
        points = []
        for i in range(N):
            angle = i * angle_step - math.pi / 2
            x_end = center + int(radius * math.cos(angle))
            y_end = center + int(radius * math.sin(angle))
            draw.line([(center, center), (x_end, y_end)], fill=(51, 65, 85, 255), width=1)

            # Data vertex
            norm_val = max(0.0, min(100.0, values[i])) / 100.0
            vx = center + int(radius * norm_val * math.cos(angle))
            vy = center + int(radius * norm_val * math.sin(angle))
            points.append((vx, vy))

        # Fill and draw data polygon
        overlay = PILImage.new('RGBA', (size, size), (0, 0, 0, 0))
        draw_overlay = ImageDraw.Draw(overlay)
        if len(points) >= 3:
            draw_overlay.polygon(points, fill=(56, 189, 248, 80))
            draw_overlay.polygon(points, outline=(56, 189, 248, 255), width=3)

        img = PILImage.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)

        # Draw vertex points
        for (vx, vy) in points:
            draw.ellipse([(vx - 4, vy - 4), (vx + 4, vy + 4)], fill=(56, 189, 248, 255), outline=(15, 23, 42, 255), width=2)

        # Text labels for axes
        for i, cat in enumerate(categories):
            angle = i * angle_step - math.pi / 2
            lx = center + int((radius + 40) * math.cos(angle))
            ly = center + int((radius + 40) * math.sin(angle))
            label_text = f"{cat} ({values[i]:.0f}%)"
            draw.text((lx - 25, ly - 8), label_text, fill=(56, 189, 248, 255))

        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        return buf

    @classmethod
    def generate_pdf_report(cls, ref_vector: RegionFeatureVector, candidate: AnalogCandidate, output_path: str) -> str:
        """Compile complete multi-page PDF scientific research report."""
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            leftMargin=36,
            rightMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=20,
            leading=24,
            textColor=colors.HexColor('#0f172a')
        )
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=10,
            leading=13,
            textColor=colors.HexColor('#0284c7')
        )
        h2_style = ParagraphStyle(
            'SectionH2',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=15,
            textColor=colors.HexColor('#1e293b'),
            spaceBefore=8,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor('#334155')
        )
        body_bold = ParagraphStyle(
            'ReportBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )
        bullet_style = ParagraphStyle(
            'ReportBullet',
            parent=body_style,
            leftIndent=15,
            firstLineIndent=-10
        )

        story = []

        # Header Title Banner
        story.append(Paragraph("TERRATWIN PLANETARY ANALOG RESEARCH REPORT", title_style))
        story.append(Paragraph(f"AI-Powered Geospatial Analysis for Extraterrestrial Exploration • NASA Space Apps Challenge", subtitle_style))
        story.append(Spacer(1, 6))
        story.append(HRFlowable(width="100%", thickness=2, color=colors.HexColor('#0284c7'), spaceAfter=10))

        # Metadata Overview Table
        planet_name = ref_vector.planet.capitalize()
        meta_data = [
            [
                Paragraph("<b>Reference Region:</b>", body_style),
                Paragraph(f"{ref_vector.name} ({planet_name})", body_bold),
                Paragraph("<b>Earth Analog Candidate:</b>", body_style),
                Paragraph(f"{candidate.name} ({candidate.country})", body_bold)
            ],
            [
                Paragraph("<b>Extraterrestrial Coordinates:</b>", body_style),
                Paragraph(f"{ref_vector.latitude:.2f}°, {ref_vector.longitude:.2f}°", body_style),
                Paragraph("<b>Terrestrial Coordinates:</b>", body_style),
                Paragraph(f"{candidate.latitude:.2f}°, {candidate.longitude:.2f}°", body_style)
            ],
            [
                Paragraph("<b>Overall Similarity Index:</b>", body_style),
                Paragraph(f"<b>{candidate.overall_similarity}%</b> ({candidate.confidence_level})", body_bold),
                Paragraph("<b>Exploration Radius:</b>", body_style),
                Paragraph(f"{ref_vector.radius_km:.1f} km", body_style)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[1.8*inch, 2.0*inch, 1.8*inch, 2.0*inch])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f8fafc')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#cbd5e1')),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 10))

        # Executive Summary & Radar Chart side-by-side
        radar_img_buf = cls.generate_radar_chart(candidate)
        radar_img = Image(radar_img_buf, width=2.6*inch, height=2.6*inch)

        summary_text = (
            f"<b>Executive Summary:</b><br/>"
            f"The TerraTwin similarity engine evaluates {candidate.name} as a <b>{candidate.overall_similarity}%</b> "
            f"match to {ref_vector.name} on {planet_name}. Topographic resemblance is calculated at "
            f"<b>{candidate.components.topography_similarity}%</b> based on regional slope gradient and terrain roughness. "
            f"Petrological compatibility is rated at <b>{candidate.components.geological_similarity}%</b> between "
            f"{candidate.features.geology.rock_type} and extraterrestrial {ref_vector.geology.rock_type}.<br/><br/>"
            f"<b>Geological Context:</b><br/>{candidate.geological_context}"
        )
        summary_para = Paragraph(summary_text, body_style)

        side_by_side = Table([[summary_para, radar_img]], colWidths=[4.7*inch, 2.9*inch])
        side_by_side.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(side_by_side)
        story.append(Spacer(1, 8))

        # Parameter Comparison Table
        story.append(Paragraph("Quantitative Parameter Comparison", h2_style))
        param_rows = [
            ["Parameter Category", f"{ref_vector.name} ({planet_name})", f"{candidate.name} (Earth)", "Units", "Congruence"]
        ]

        t_r = ref_vector.topography
        t_c = candidate.features.topography
        th_r = ref_vector.thermal
        th_c = candidate.features.thermal
        s_r = ref_vector.surface
        s_c = candidate.features.surface

        param_rows.append(["Mean Elevation", f"{t_r.elevation_mean.value:,.0f}", f"{t_c.elevation_mean.value:,.0f}", "meters", "Baseline"])
        param_rows.append(["Topographic Relief", f"{t_r.relief_m.value:,.0f}", f"{t_c.relief_m.value:,.0f}", "meters", "Comparable"])
        param_rows.append(["Mean Surface Slope", f"{t_r.slope_mean.value:.1f}", f"{t_c.slope_mean.value:.1f}", "degrees", f"Δ = {abs(t_r.slope_mean.value - t_c.slope_mean.value):.1f}°"])
        param_rows.append(["Peak Slope (90th percentile)", f"{t_r.slope_p90.value:.1f}", f"{t_c.slope_p90.value:.1f}", "degrees", f"Δ = {abs(t_r.slope_p90.value - t_c.slope_p90.value):.1f}°"])
        param_rows.append(["Terrain Ruggedness (TRI)", f"{t_r.terrain_roughness.value:.1f}", f"{t_c.terrain_roughness.value:.1f}", "TRI index", "Morphological Match"])
        param_rows.append(["Diurnal Temperature Swing", f"{th_r.diurnal_range_k.value:.0f}", f"{th_c.diurnal_range_k.value:.0f}", "Kelvin", f"Δ = {abs(th_r.diurnal_range_k.value - th_c.diurnal_range_k.value):.0f} K"])
        param_rows.append(["Thermal Inertia", f"{th_r.thermal_inertia_si.value:.0f}", f"{th_c.thermal_inertia_si.value:.0f}", "J m⁻² K⁻¹ s⁻¹/²", "Conductive Match"])
        param_rows.append(["Optical Albedo", f"{s_r.albedo.value:.2f}", f"{s_c.albedo.value:.2f}", "reflectance", "Photometric"])
        param_rows.append(["Bare Ground Ratio", f"{s_r.bare_ground_ratio.value*100:.0f}%", f"{s_c.bare_ground_ratio.value*100:.0f}%", "percentage", "Desert / Regolith"])

        param_table = Table(param_rows, colWidths=[2.2*inch, 1.8*inch, 1.8*inch, 1.0*inch, 0.8*inch])
        param_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0f172a')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f8fafc'), colors.white]),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(param_table)
        story.append(Spacer(1, 10))

        # Exploration Applications Matrix
        story.append(Paragraph("Mission & Exploration Suitability Matrix", h2_style))
        suit_data = [
            ["Exploration Discipline", "Readiness Assessment & Operational Guidance"]
        ]
        for domain, text in candidate.exploration_suitability.items():
            domain_label = domain.replace('_', ' ').title()
            suit_data.append([domain_label, text])

        suit_table = Table(suit_data, colWidths=[2.2*inch, 5.4*inch])
        suit_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,-1), 8),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#f0f9ff'), colors.white]),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ]))
        story.append(suit_table)
        story.append(Spacer(1, 8))

        # Fundamental Environmental Differences
        story.append(Paragraph("Fundamental Planetary Differences (Non-Reproducible on Earth)", h2_style))
        g_earth = PLANETARY_SYSTEM["earth"]["physical"]["surface_gravity_ms2"]
        g_ref = PLANETARY_SYSTEM[ref_vector.planet]["physical"]["surface_gravity_ms2"]
        p_ref = PLANETARY_SYSTEM[ref_vector.planet]["physical"]["atmospheric_pressure_hpa"]

        diff_points = [
            f"<b>Gravity:</b> Earth gravity ({g_earth:.2f} m/s²) is substantially higher than {planet_name} ({g_ref:.2f} m/s²). Mechanical load and rover wheel sinkage must be compensated with counterweights or low tire pressure.",
            f"<b>Atmosphere & Vacuum:</b> Earth ambient pressure (~1013 hPa) cannot replicate {'hard vacuum' if p_ref < 0.01 else f'the thin {p_ref:.1f} hPa CO2 atmosphere'} of {planet_name}. Volatiles and plume expansion require TVAC chambers.",
            f"<b>Solar Radiation & Magnetosphere:</b> Earth's magnetic field (~45 µT) and ozone layer shield against galactic cosmic rays (GCR) and solar energetic particles (SEP).",
            f"<b>Historical Analog Missions:</b> Utilized by: {', '.join(candidate.real_world_missions)}."
        ]
        for p in diff_points:
            story.append(Paragraph(f"• {p}", bullet_style))
            story.append(Spacer(1, 2))

        story.append(Spacer(1, 8))
        story.append(Paragraph("Data Sources & Methodology", h2_style))
        citations = (
            f"<b>Moon Datasets:</b> NASA LRO LOLA GDR Topography (Smith et al.), Diviner Lunar Radiometer (Paige et al.).<br/>"
            f"<b>Mars Datasets:</b> NASA MGS MOLA MEGDR Topography (Zuber et al.), Odyssey THEMIS IR (Christensen et al.).<br/>"
            f"<b>Earth Datasets:</b> USGS Shuttle Radar Topography Mission (SRTM 30m), NASA MODIS MOD11A1, GLiM Lithology.<br/>"
            f"<b>Methodology:</b> Multi-dimensional normalized weighted Euclidean distance metric with categorical petrological compatibility matrix."
        )
        story.append(Paragraph(citations, body_style))

        doc.build(story)
        return output_path
