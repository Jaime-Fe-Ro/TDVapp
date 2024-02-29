from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import Portfolios
from . import db

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    portfolios = Portfolios.query.filter_by(user_id=current_user.id).all()
    return render_template("home.html", user=current_user, portfolios=portfolios)


@views.route('/new-portfolio', methods=['GET', 'POST'])
@login_required
def new_portfolio():
    if request.method == 'POST':
        portfolio_name = request.form.get('portfolio')
        if portfolio_name == "":
            portfolio_name = "69420 - should have named the Portfolio lol"
        cash = request.form.get('cash')
        shares = request.form.get('shares')

        new_portfolio_info = Portfolios(portfolio_name=portfolio_name, cash=cash, shares=shares, user_id=current_user.id)
        db.session.add(new_portfolio_info)
        db.session.commit()

        return redirect('/')

    return render_template("new_portfolio.html", user=current_user)
