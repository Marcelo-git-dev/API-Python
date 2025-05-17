from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import database as db

app = Flask(__name__)

@app.template_filter('format_date')
def format_date_filter(value):
    try:
        if isinstance(value, str):
            date_obj = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        else:
            date_obj = value
        
        return date_obj.strftime('%d/%m/%Y %H:%M')
    except:
        return value

@app.template_filter('capitalize')
def capitalize_filter(value):
    return value.capitalize() if value else ''

@app.route('/')
def index():
    membros = db.get_membros()
    eventos = db.get_eventos()
    return render_template('index.html', membros=membros, eventos=eventos)

@app.route('/registrar_presenca', methods=['POST'])
def registrar_presenca():
    membro_id = request.form.get('membro_id')
    evento_id = request.form.get('evento_id')
    presente = request.form.get('presente') == 'true'
    
    db.registrar_presenca(membro_id, evento_id, presente)
    return jsonify({'success': True})

@app.route('/adicionar_membro', methods=['GET', 'POST'])
def adicionar_membro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        funcao = request.form.get('funcao')
        
        if nome:
            db.adicionar_membro(nome, funcao)
            return redirect(url_for('index'))
    
    return render_template('adicionar_membro.html')

@app.route('/adicionar_evento', methods=['GET', 'POST'])
def adicionar_evento():
    if request.method == 'POST':
        nome = request.form.get('nome')
        data = request.form.get('data')
        tipo = request.form.get('tipo')
        
        if nome and data and tipo:
            db.adicionar_evento(nome, data, tipo)
            return redirect(url_for('index'))
    
    return render_template('adicionar_evento.html')

@app.route('/relatorios')
def relatorios():
    try:
        membros = db.get_membros()
        eventos = db.get_eventos()
        presencas = db.get_presencas()
        
        metricas = []
        for membro in membros:
            eventos_do_membro = [p for p in presencas if p['membro_id'] == membro['id']]
            total_eventos = len(eventos)
            presentes = sum(1 for p in eventos_do_membro if p['presente'])
            faltas = total_eventos - presentes if total_eventos > 0 else 0
            percentual_presenca = (presentes / total_eventos * 100) if total_eventos > 0 else 0
            
            metricas.append({
                'id': membro['id'],
                'nome': membro['nome'],
                'funcao': membro.get('funcao', ''),
                'presentes': presentes,
                'faltas': faltas,
                'percentual_presenca': round(percentual_presenca, 2),
                'ultima_presenca': max([p['evento_id'] for p in eventos_do_membro], default=0)
            })
        
        metricas_eventos = []
        for evento in eventos:
            presencas_evento = [p for p in presencas if p['evento_id'] == evento['id']]
            total_membros = len(membros)
            presentes = sum(1 for p in presencas_evento if p['presente'])
            percentual_presenca = (presentes / total_membros * 100) if total_membros > 0 else 0
            
            metricas_eventos.append({
                'id': evento['id'],
                'nome': evento['nome'],
                'data': evento['data'],
                'tipo': evento['tipo'],
                'presentes': presentes,
                'faltas': total_membros - presentes,
                'percentual_presenca': round(percentual_presenca, 2)
            })
        
        metricas_ordenadas = sorted(metricas, key=lambda x: x['percentual_presenca'], reverse=True)
        metricas_eventos_ordenadas = sorted(metricas_eventos, key=lambda x: x['data'], reverse=True)
        
        return render_template(
            'relatorios.html',
            metricas=metricas_ordenadas,
            metricas_eventos=metricas_eventos_ordenadas,
            total_membros=len(membros),
            total_eventos=len(eventos)
        )
    
    except Exception as e:
        print(f"Erro ao gerar relatórios: {str(e)}")
        return render_template('error.html', error_message="Ocorreu um erro ao gerar os relatórios.")

if __name__ == '__main__':
    app.run(debug=True)