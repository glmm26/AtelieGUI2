import os
from flask import Flask, render_template
from flask_login import LoginManager
from atelie_online.models import db
from atelie_online.models.usuario import Usuario
from atelie_online.controllers.auth_controller import auth_bp
from atelie_online.controllers.cliente_controller import cliente_bp
from atelie_online.controllers.servico_controller import servico_bp
from atelie_online.controllers.material_controller import material_bp

def create_app():
    app = Flask(__name__, template_folder='atelie_online/templates', static_folder='atelie_online/static')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@db:5432/atelie_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.environ.get('SECRET_KEY', 'troque_essa_chave')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(cliente_bp, url_prefix='/clientes')
    app.register_blueprint(servico_bp, url_prefix='/servicos')
    app.register_blueprint(material_bp, url_prefix='/material')

    @app.route('/')
    def home():
        # If the app is using session-based login (session['usuario_id']), prefer that user
        from flask import session
        from flask_login import current_user as flask_current_user

        user_obj = None
        try:
            if 'usuario_id' in session:
                user_obj = Usuario.query.get(int(session['usuario_id']))
        except Exception:
            user_obj = None

        # pass a user-like object named current_user to keep templates unchanged
        resolved = (user_obj or flask_current_user)
        # debug: print which user object was resolved for the template
        try:
            print(f"Home current_user resolved: id={(resolved.id if resolved and hasattr(resolved,'id') else None)}, foto={(resolved.foto if resolved and hasattr(resolved,'foto') else None)}")
        except Exception:
            pass
        return render_template('index.html', current_user=resolved)

    @app.route('/admin_dashboard')
    def admin_dashboard():
        from flask import session, redirect, url_for, render_template

        #tirar estes comentário quando login ok - é apenas para ver css do admin
        #if 'usuario_id' not in session or not session.get('is_admin'):
            #return redirect(url_for('auth.login'))
        return render_template('admin_dashboard.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
