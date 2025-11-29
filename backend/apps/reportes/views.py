from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
import json
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas
from .serializers import ReporteSaludSerializer, ReporteSocialSerializer, ReporteEncuestasSerializer
from apps.usuarios.permissions import EsAdminRol

class BaseReporteViewSet(viewsets.ModelViewSet):
    """
    ViewSet base para reportes.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

    def _generate_pdf(self, reporte, tipo):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Título
        title = Paragraph(f"Reporte de {tipo.title()}", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))

        # Información básica
        info_data = [
            ['Tipo de Reporte:', reporte.tipo_reporte],
            ['Fecha del Reporte:', reporte.fecha_reporte.strftime('%Y-%m-%d')],
            ['Generado por:', f"{reporte.generado_por.first_name} {reporte.generado_por.last_name} ({reporte.generado_por.username})"],
            ['Fecha de Creación:', reporte.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')]
        ]

        info_table = Table(info_data, colWidths=[100, 300])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 12))

        # Datos agregados
        if reporte.datos_agregados:
            datos = reporte.datos_agregados
            story.append(Paragraph("Datos Agregados:", styles['Heading2']))
            story.append(Spacer(1, 12))

            if tipo == 'salud':
                # Tabla de registros de salud
                if 'registros_salud' in datos and datos['registros_salud']:
                    story.append(Paragraph("Registros de Salud:", styles['Heading3']))
                    registros_data = [['Fecha', 'Tipo', 'Descripción', 'Observaciones']]
                    for reg in datos['registros_salud'][:10]:  # Limitar a 10 registros
                        registros_data.append([
                            reg.get('fecha_registro', ''),
                            reg.get('tipo_registro', ''),
                            reg.get('descripcion', '')[:50] + '...' if len(reg.get('descripcion', '')) > 50 else reg.get('descripcion', ''),
                            reg.get('observaciones', '')[:50] + '...' if len(reg.get('observaciones', '')) > 50 else reg.get('observaciones', '')
                        ])
                    registros_table = Table(registros_data, colWidths=[80, 80, 150, 150])
                    registros_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(registros_table)
                    story.append(Spacer(1, 12))

                # Estadísticas
                stats_data = [
                    ['Total Registros:', str(datos.get('total_registros', 0))],
                    ['Total Alertas:', str(datos.get('total_alertas', 0))],
                    ['Alertas Activas:', str(datos.get('alertas_activas', 0))],
                    ['Controles Pendientes:', str(datos.get('controles_pendientes', 0))]
                ]
                stats_table = Table(stats_data, colWidths=[150, 100])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_table)

            elif tipo == 'social':
                # Tabla de programas
                if 'programas_beneficiario' in datos and datos['programas_beneficiario']:
                    story.append(Paragraph("Programas del Beneficiario:", styles['Heading3']))
                    programas_data = [['Programa', 'Fecha Inscripción', 'Estado']]
                    for prog in datos['programas_beneficiario'][:10]:
                        programas_data.append([
                            prog.get('programa__nombre', ''),
                            prog.get('fecha_inscripcion', ''),
                            prog.get('estado', '')
                        ])
                    programas_table = Table(programas_data, colWidths=[150, 100, 80])
                    programas_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(programas_table)
                    story.append(Spacer(1, 12))

                # Estadísticas sociales
                stats_social_data = [
                    ['Total Programas:', str(datos.get('total_programas', 0))],
                    ['Programas Activos:', str(datos.get('programas_activos', 0))],
                    ['Programas Egresados:', str(datos.get('programas_egresados', 0))]
                ]
                stats_social_table = Table(stats_social_data, colWidths=[150, 100])
                stats_social_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_social_table)

            elif tipo == 'encuestas':
                # Tabla de respuestas
                if 'respuestas_detalladas' in datos and datos['respuestas_detalladas']:
                    story.append(Paragraph("Respuestas a Encuestas:", styles['Heading3']))
                    respuestas_data = [['Encuesta', 'Pregunta', 'Respuesta']]
                    for resp in datos['respuestas_detalladas'][:10]:
                        respuestas_data.append([
                            resp.get('encuesta__titulo', '')[:30] + '...' if len(resp.get('encuesta__titulo', '')) > 30 else resp.get('encuesta__titulo', ''),
                            resp.get('pregunta__texto_pregunta', '')[:40] + '...' if len(resp.get('pregunta__texto_pregunta', '')) > 40 else resp.get('pregunta__texto_pregunta', ''),
                            resp.get('opcion__texto_opcion', '') or resp.get('respuesta_texto', '')[:30] + '...' if len(resp.get('respuesta_texto', '')) > 30 else resp.get('respuesta_texto', '')
                        ])
                    respuestas_table = Table(respuestas_data, colWidths=[100, 150, 100])
                    respuestas_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(respuestas_table)
                    story.append(Spacer(1, 12))

                # Estadísticas de encuestas
                stats_encuestas_data = [
                    ['Total Respuestas:', str(datos.get('total_respuestas_persona', 0))],
                    ['Encuestas Activas:', str(datos.get('estadisticas_generales', {}).get('encuestas_activas', 0))],
                    ['Total Preguntas:', str(datos.get('estadisticas_generales', {}).get('total_preguntas', 0))]
                ]
                stats_encuestas_table = Table(stats_encuestas_data, colWidths=[150, 100])
                stats_encuestas_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_encuestas_table)

        doc.build(story)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{tipo}_{reporte.id}.pdf"'
        return response

# Vista para Reportes de Salud
class ReporteSaludViewSet(BaseReporteViewSet):
    queryset = ReporteSalud.objects.all()
    serializer_class = ReporteSaludSerializer

    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        reporte = self.get_object()
        return self._generate_pdf(reporte, 'salud')

# Vista para Reportes Sociales
class ReporteSocialViewSet(BaseReporteViewSet):
    queryset = ReporteSocial.objects.all()
    serializer_class = ReporteSocialSerializer

    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        reporte = self.get_object()
        return self._generate_pdf(reporte, 'social')

# Vista para Reportes de Encuestas
class ReporteEncuestasViewSet(BaseReporteViewSet):
    queryset = ReporteEncuestas.objects.all()
    serializer_class = ReporteEncuestasSerializer

    @action(detail=True, methods=['get'])
    def export_pdf(self, request, pk=None):
        reporte = self.get_object()
        return self._generate_pdf(reporte, 'encuestas')

    def _generate_pdf(self, reporte, tipo):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        # Título
        title = Paragraph(f"Reporte de {tipo.title()}", styles['Title'])
        story.append(title)
        story.append(Spacer(1, 12))

        # Información básica
        info_data = [
            ['Tipo de Reporte:', reporte.tipo_reporte],
            ['Fecha del Reporte:', reporte.fecha_reporte.strftime('%Y-%m-%d')],
            ['Generado por:', f"{reporte.generado_por.first_name} {reporte.generado_por.last_name} ({reporte.generado_por.username})"],
            ['Fecha de Creación:', reporte.fecha_creacion.strftime('%Y-%m-%d %H:%M:%S')]
        ]

        info_table = Table(info_data, colWidths=[100, 300])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 12))

        # Datos agregados
        if reporte.datos_agregados:
            datos = reporte.datos_agregados
            story.append(Paragraph("Datos Agregados:", styles['Heading2']))
            story.append(Spacer(1, 12))

            if tipo == 'salud':
                # Tabla de registros de salud
                if 'registros_salud' in datos and datos['registros_salud']:
                    story.append(Paragraph("Registros de Salud:", styles['Heading3']))
                    registros_data = [['Fecha', 'Tipo', 'Descripción', 'Observaciones']]
                    for reg in datos['registros_salud'][:10]:  # Limitar a 10 registros
                        registros_data.append([
                            reg.get('fecha_registro', ''),
                            reg.get('tipo_registro', ''),
                            reg.get('descripcion', '')[:50] + '...' if len(reg.get('descripcion', '')) > 50 else reg.get('descripcion', ''),
                            reg.get('observaciones', '')[:50] + '...' if len(reg.get('observaciones', '')) > 50 else reg.get('observaciones', '')
                        ])
                    registros_table = Table(registros_data, colWidths=[80, 80, 150, 150])
                    registros_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(registros_table)
                    story.append(Spacer(1, 12))

                # Estadísticas
                stats_data = [
                    ['Total Registros:', str(datos.get('total_registros', 0))],
                    ['Total Alertas:', str(datos.get('total_alertas', 0))],
                    ['Alertas Activas:', str(datos.get('alertas_activas', 0))],
                    ['Controles Pendientes:', str(datos.get('controles_pendientes', 0))]
                ]
                stats_table = Table(stats_data, colWidths=[150, 100])
                stats_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_table)

            elif tipo == 'social':
                # Tabla de programas
                if 'programas_beneficiario' in datos and datos['programas_beneficiario']:
                    story.append(Paragraph("Programas del Beneficiario:", styles['Heading3']))
                    programas_data = [['Programa', 'Fecha Inscripción', 'Estado']]
                    for prog in datos['programas_beneficiario'][:10]:
                        programas_data.append([
                            prog.get('programa__nombre', ''),
                            prog.get('fecha_inscripcion', ''),
                            prog.get('estado', '')
                        ])
                    programas_table = Table(programas_data, colWidths=[150, 100, 80])
                    programas_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(programas_table)
                    story.append(Spacer(1, 12))

                # Estadísticas sociales
                stats_social_data = [
                    ['Total Programas:', str(datos.get('total_programas', 0))],
                    ['Programas Activos:', str(datos.get('programas_activos', 0))],
                    ['Programas Egresados:', str(datos.get('programas_egresados', 0))]
                ]
                stats_social_table = Table(stats_social_data, colWidths=[150, 100])
                stats_social_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightgreen),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_social_table)

            elif tipo == 'encuestas':
                # Tabla de respuestas
                if 'respuestas_detalladas' in datos and datos['respuestas_detalladas']:
                    story.append(Paragraph("Respuestas a Encuestas:", styles['Heading3']))
                    respuestas_data = [['Encuesta', 'Pregunta', 'Respuesta']]
                    for resp in datos['respuestas_detalladas'][:10]:
                        respuestas_data.append([
                            resp.get('encuesta__titulo', '')[:30] + '...' if len(resp.get('encuesta__titulo', '')) > 30 else resp.get('encuesta__titulo', ''),
                            resp.get('pregunta__texto_pregunta', '')[:40] + '...' if len(resp.get('pregunta__texto_pregunta', '')) > 40 else resp.get('pregunta__texto_pregunta', ''),
                            resp.get('opcion__texto_opcion', '') or resp.get('respuesta_texto', '')[:30] + '...' if len(resp.get('respuesta_texto', '')) > 30 else resp.get('respuesta_texto', '')
                        ])
                    respuestas_table = Table(respuestas_data, colWidths=[100, 150, 100])
                    respuestas_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('FONTSIZE', (0, 0), (-1, 0), 8),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)
                    ]))
                    story.append(respuestas_table)
                    story.append(Spacer(1, 12))

                # Estadísticas de encuestas
                stats_encuestas_data = [
                    ['Total Respuestas:', str(datos.get('total_respuestas_persona', 0))],
                    ['Encuestas Activas:', str(datos.get('estadisticas_generales', {}).get('encuestas_activas', 0))],
                    ['Total Preguntas:', str(datos.get('estadisticas_generales', {}).get('total_preguntas', 0))]
                ]
                stats_encuestas_table = Table(stats_encuestas_data, colWidths=[150, 100])
                stats_encuestas_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightyellow),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(stats_encuestas_table)

        doc.build(story)
        buffer.seek(0)

        response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="reporte_{tipo}_{reporte.id}.pdf"'
        return response
