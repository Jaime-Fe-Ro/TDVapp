from flask import Blueprint, render_template, request, redirect, flash
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
        cash = request.form.get('cash')
        shares = request.form.get('shares')

        existing_portfolio = Portfolios.query.filter_by(user_id=current_user.id, portfolio_name=portfolio_name).first()
        if existing_portfolio:
            flash('A portfolio with this name already exists. Please choose a different name.', 'error')
            # Note: Not passing portfolio_name back to the template on error
            return render_template("new_portfolio.html", user=current_user, cash=cash, shares=shares)

        new_portfolio_info = Portfolios(portfolio_name=portfolio_name, cash=cash, shares=shares, user_id=current_user.id)
        db.session.add(new_portfolio_info)
        db.session.commit()

        return redirect('/')

    return render_template("new_portfolio.html", user=current_user, cash="", shares="")


@views.route('/delete-portfolio', methods=['POST'])
@login_required
def delete_portfolio():
    portfolio_id = request.form.get('portfolio_id')
    portfolio = Portfolios.query.filter_by(id=portfolio_id).first()
    if portfolio:
        if portfolio.user_id == current_user.id:
            portfolio_name = portfolio.portfolio_name
            db.session.delete(portfolio)
            db.session.commit()
            flash(f'Portfolio "{portfolio_name}" successfully deleted!', 'success')
    return redirect('/')


@views.route('/modify-portfolio/<int:portfolio_id>', methods=['GET', 'POST'])
@login_required
def modify_portfolio(portfolio_id):
    portfolio = Portfolios.query.get_or_404(portfolio_id)
    if request.method == 'POST':
        portfolio.cash = request.form['cash']
        portfolio.shares = request.form['shares']
        portfolio.portfolio_name = request.form['portfolio']
        db.session.commit()
        return redirect('/')
    return render_template("modify_portfolio.html", user=current_user, portfolio=portfolio)
