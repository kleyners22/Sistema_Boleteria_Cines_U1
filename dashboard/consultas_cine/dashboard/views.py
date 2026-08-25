import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from django.db import connections
from django.shortcuts import render


def generar_graficas():
    graficos = {}

    plt.rcParams.update({
        'font.family': 'sans-serif',
        'axes.spines.top': False,
        'axes.spines.right': False,
    })

    with connections['default'].cursor() as cursor:
        cursor.execute("""
            SELECT b.fecha, b.numero_sala, b.id_pelicula,
                   t.nombre AS tipo_boleto, t.precio,
                   b.asiento, b.cedula_cliente
            FROM boleto b
            JOIN tipo_boleto t ON b.id_tipo_boleto = t.id_tipo_boleto
        """)
        columnas = [col[0] for col in cursor.description]
        filas = cursor.fetchall()

    df = pd.DataFrame(filas, columns=columnas)

    # 1. Boletos vendidos por tipo (barras)
    conteo_tipo = df['tipo_boleto'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    colores = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63']
    bars = ax.bar(conteo_tipo.index, conteo_tipo.values, color=colores[:len(conteo_tipo)], edgecolor='white', linewidth=1.2)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.15,
                str(int(bar.get_height())), ha='center', va='bottom', fontweight='bold', fontsize=12)
    ax.set_title('Boletos Vendidos por Tipo', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Tipo de Boleto', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cantidad', fontsize=12, fontweight='bold')
    ax.tick_params(axis='both', labelsize=11)
    ax.grid(axis='y', alpha=0.2, linestyle='--')
    plt.tight_layout()
    graficos['Boletos por Tipo'] = _a_base64(fig)
    plt.close(fig)

    # 2. Ingresos totales por dia (barras)
    df['fecha'] = pd.to_datetime(df['fecha'])
    df['precio'] = pd.to_numeric(df['precio'])
    ingresos_fecha = df.groupby(df['fecha'].dt.strftime('%Y-%m-%d'))['precio'].sum()
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    bars = ax.bar(ingresos_fecha.index, ingresos_fecha.values, color='#9C27B0', edgecolor='white', linewidth=1.2, width=0.6)
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.3,
                f'${bar.get_height():.2f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax.set_title('Ingresos Totales por Dia', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
    ax.set_ylabel('Ingresos ($)', fontsize=12, fontweight='bold')
    ax.set_xticklabels(ingresos_fecha.index, rotation=45, ha='right', fontsize=11, fontweight='bold')
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(axis='y', alpha=0.2, linestyle='--')
    plt.tight_layout()
    graficos['Ingresos por Dia'] = _a_base64(fig)
    plt.close(fig)

    # 3. Distribucion por sala (pie)
    conteo_sala = df['numero_sala'].value_counts().sort_index()
    fig, ax = plt.subplots(figsize=(7, 7))
    fig.patch.set_facecolor('#f8f9fa')
    colores_pie = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0', '#00BCD4', '#795548', '#607D8B', '#F44336', '#3F51B5']
    wedges, texts, autotexts = ax.pie(
        conteo_sala.values,
        labels=[f'Sala {s}' for s in conteo_sala.index],
        autopct='%1.1f%%',
        colors=colores_pie[:len(conteo_sala)],
        startangle=90,
        textprops={'fontsize': 11, 'fontweight': 'bold'},
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    for t in autotexts:
        t.set_fontweight('bold')
        t.set_fontsize(10)
    ax.set_title('Distribucion de Boletos por Sala', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    graficos['Boletos por Sala'] = _a_base64(fig)
    plt.close(fig)

    # 4. Top peliculas mas vendidas (barras)
    conteo_pelicula = df['id_pelicula'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor('#f8f9fa')
    ax.set_facecolor('#f8f9fa')
    bars = ax.bar(range(len(conteo_pelicula)), conteo_pelicula.values, color='#FF5722', edgecolor='white', linewidth=1.2, width=0.6)
    ax.set_xticks(range(len(conteo_pelicula)))
    ax.set_xticklabels([f'Pelicula {pid}' for pid in conteo_pelicula.index], rotation=30, ha='right', fontsize=10, fontweight='bold')
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.15,
                str(int(bar.get_height())), ha='center', va='bottom', fontweight='bold', fontsize=12)
    ax.set_title('Top Peliculas mas Vendidas', fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Pelicula', fontsize=12, fontweight='bold')
    ax.set_ylabel('Boletos Vendidos', fontsize=12, fontweight='bold')
    ax.tick_params(axis='both', labelsize=10)
    ax.grid(axis='y', alpha=0.2, linestyle='--')
    plt.tight_layout()
    graficos['Top Peliculas'] = _a_base64(fig)
    plt.close(fig)

    total_boletos = len(df)
    ingresos = float(df['precio'].sum())
    peliculas = df['id_pelicula'].nunique()
    clientes = df['cedula_cliente'].nunique()

    stats = {
        'total_boletos': total_boletos,
        'ingresos': f'{ingresos:.2f}',
        'peliculas': peliculas,
        'clientes': clientes,
    }

    return graficos, stats


def _a_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    imagen = base64.b64encode(buffer.read()).decode('utf-8')
    return imagen


def dashboard_view(request):
    graficos, stats = generar_graficas()
    return render(request, 'consulta.html', {'graficos': graficos, **stats})
