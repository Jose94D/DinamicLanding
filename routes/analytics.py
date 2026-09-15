from flask import Blueprint, render_template
from flask_login import login_required
from extensions import get_db_connection

analytics_bp = Blueprint('analytics', __name__, url_prefix='/admin')


@analytics_bp.route('/analiticas')
@login_required
def analiticas():
    conn = get_db_connection()

    total_visitas = conn.execute(
        'SELECT COUNT(*) as total FROM analiticas_visitas'
    ).fetchone()['total']

    # Desglose mensual (para el gráfico de líneas)
    por_mes = conn.execute('''
        SELECT strftime('%Y-%m', fecha) AS periodo, COUNT(*) AS total
        FROM analiticas_visitas
        GROUP BY periodo
        ORDER BY periodo ASC
    ''').fetchall()

    # Desglose anual (para la tabla resumen)
    por_anio = conn.execute('''
        SELECT strftime('%Y', fecha) AS anio, COUNT(*) AS total
        FROM analiticas_visitas
        GROUP BY anio
        ORDER BY anio ASC
    ''').fetchall()

    # Páginas más visitadas
    paginas_top = conn.execute('''
        SELECT ruta, COUNT(*) AS total
        FROM analiticas_visitas
        GROUP BY ruta
        ORDER BY total DESC
        LIMIT 10
    ''').fetchall()

    conn.close()

    return render_template(
        'admin/analiticas.html',
        total_visitas=total_visitas,
        por_mes=por_mes,
        por_anio=por_anio,
        paginas_top=paginas_top
    )