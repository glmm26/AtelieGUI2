from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import current_user, login_required
from atelie_online.models.servico_model import Servico
from atelie_online.models.usuario import Usuario
from atelie_online.models import db
from flask import session

servico_bp = Blueprint('servicos', __name__, template_folder='../templates')

def get_current_user():
    """Retorna o usuário logado considerando session ou flask_login"""
    user_obj = None
    try:
        if 'usuario_id' in session:
            user_obj = Usuario.query.get(int(session['usuario_id']))
        else:
            user_obj = current_user if current_user.is_authenticated else None
    except Exception:
        user_obj = None
    return user_obj

@servico_bp.route('/')
def index():
    return redirect(url_for('servicos.cadastrar_servico'))

@servico_bp.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar_servico():
    if request.method == 'POST':
        nome_cliente = request.form.get('nome_cliente')
        tipo_servico = request.form.get('tipo_servico')
        descricao = request.form.get('descricao')

        novo_servico = Servico(None, nome_cliente, tipo_servico, descricao)
        try:
            db.session.add(novo_servico)
            db.session.commit()
            flash('Serviço cadastrado com sucesso!', 'success')
            return redirect(url_for('servicos.listar_servicos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao cadastrar serviço: {str(e)}', 'danger')
            return redirect(url_for('servicos.cadastrar_servico'))

    return render_template('cadastro_servico.html')

@servico_bp.route('/servicos')
def listar_servicos():
    servicos = Servico.query.all()
    return render_template('lista_servicos.html', servicos=servicos)

@servico_bp.route('/excluir/<int:id>', methods=['POST'])
def excluir_servico(id):
    servico = Servico.query.get_or_404(id)
    try:
        db.session.delete(servico)
        db.session.commit()
        flash('Serviço excluído com sucesso!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Erro ao excluir serviço: {str(e)}', 'danger')
    return redirect(url_for('servicos.listar_servicos'))

@servico_bp.route('/projeto')
def projeto():
    return render_template('projeto.html')

@servico_bp.route('/customizacao', methods=['GET', 'POST'])
def customizacao():
    if request.method == 'POST':
        user = get_current_user()
        material = request.form.get('material')
        descricao = request.form.get('descricao', '')
        
        if not material:
            flash('Por favor, selecione um material', 'danger')
            return redirect(url_for('servicos.customizacao'))
        
        # Criar pedido de customização
        if user:
            novo_pedido = Servico(
                usuario_id=user.id,
                nome_cliente=user.nome,
                tipo_servico='Customização',
                descricao=descricao or f'Material: {material}',
                material=material
            )
            try:
                db.session.add(novo_pedido)
                db.session.commit()
                flash('✅ Pedido de customização realizado com sucesso!', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar pedido: {str(e)}', 'danger')
        else:
            flash('Você precisa estar logado para fazer um pedido', 'warning')
            return redirect(url_for('auth.login'))
    
    return render_template('customizacao.html')

@servico_bp.route('/conserto', methods=['GET', 'POST'])
def conserto():
    if request.method == 'POST':
        user = get_current_user()
        material = request.form.get('material')
        descricao = request.form.get('descricao', '')
        
        if not material:
            flash('Por favor, selecione um material', 'danger')
            return redirect(url_for('servicos.conserto'))
        
        # Criar pedido de conserto
        if user:
            novo_pedido = Servico(
                usuario_id=user.id,
                nome_cliente=user.nome,
                tipo_servico='Conserto',
                descricao=descricao or f'Material: {material}',
                material=material
            )
            try:
                db.session.add(novo_pedido)
                db.session.commit()
                flash('✅ Pedido de conserto realizado com sucesso!', 'success')
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                flash(f'Erro ao criar pedido: {str(e)}', 'danger')
        else:
            flash('Você precisa estar logado para fazer um pedido', 'warning')
            return redirect(url_for('auth.login'))
    
    return render_template('conserto.html')

@servico_bp.route('/estamparia', methods=['GET', 'POST'])
def estamparia():
    if request.method == 'POST':
        user = get_current_user()
        imagem = request.files.get('imagem')
        descricao = request.form.get('descricao', '')
        
        if not user:
            flash('Você precisa estar logado para fazer um pedido', 'warning')
            return redirect(url_for('auth.login'))
        
        # Criar pedido de estamparia
        novo_pedido = Servico(
            usuario_id=user.id,
            nome_cliente=user.nome,
            tipo_servico='Estamparia',
            descricao=descricao or 'Pedido de estampa enviado',
        )
        try:
            db.session.add(novo_pedido)
            db.session.commit()
            flash('✅ Pedido de estamparia realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar pedido: {str(e)}', 'danger')
    
    return render_template('estamparia.html')

@servico_bp.route('/material')
def material():
    return render_template('mat_cons.html')


@servico_bp.route('/api/meus-pedidos', methods=['GET'])
def api_meus_pedidos():
    """API endpoint para retornar os pedidos do usuário logado em JSON"""
    user = get_current_user()
    
    if not user:
        return jsonify({
            'success': False,
            'error': 'Usuário não autenticado'
        }), 401
    
    try:
        # Buscar todos os pedidos do usuário
        pedidos = Servico.query.filter_by(usuario_id=user.id).order_by(Servico.data_pedido.desc()).all()
        
        pedidos_data = []
        for pedido in pedidos:
            pedidos_data.append({
                'id': pedido.id,
                'tipo_servico': pedido.tipo_servico,
                'descricao': pedido.descricao,
                'status': pedido.status,
                'material': pedido.material,
                'data_pedido': pedido.data_pedido.isoformat()
            })
        
        return jsonify({
            'success': True,
            'pedidos': pedidos_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
