# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from datetime import datetime
import database as db

app = Flask(__name__)

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

@app.route('/relatorios')
def relatorios():
    # Dados para relatórios
    membros = db.get_membros()
    eventos = db.get_eventos()
    presencas = db.get_presencas()
    
    # Calcular métricas
    metricas = {}
    for membro in membros:
        total_eventos = len(eventos)
        presentes = sum(1 for p in presencas if p['membro_id'] == membro['id'] and p['presente'])
        faltas = total_eventos - presentes
        percentual_presenca = (presentes / total_eventos) * 100 if total_eventos > 0 else 0
        
        metricas[membro['id']] = {
            'nome': membro['nome'],
            'presentes': presentes,
            'faltas': faltas,
            'percentual_presenca': round(percentual_presenca, 2)
        }
    
    return render_template('relatorios.html', metricas=metricas, eventos=eventos)

if __name__ == '__main__':
    app.run(debug=True)