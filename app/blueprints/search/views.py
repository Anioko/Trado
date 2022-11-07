from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required
from flask_sqlalchemy.pagination import QueryPagination
from sqlalchemy import desc, func
from app import db
from app.models import *
from app.blueprints.search.forms import *

search = Blueprint('search', __name__)


@search.route('/test')
def test():
    test_search = User.query.whooshee_search(
        'Shawn').order_by(User.id.desc()).first()
    return render_template("search/search_test.html", test_search=test_search)


@search.route('/')
def index():

    query = request.args.get('query')
    page = request.args.get('page')
    search_type = request.args.get('type')
    sort_by = request.args.get('sort_by')
    sort_dir = request.args.get('sort_dir')

    query = query if query is not None else ''
    page = page if page is not None else 1

    try:
        page = int(page)
    except:
        page = 1
    search_type = search_type if search_type is not None else ''
    sort_by = sort_by if sort_by is not None else ''
    sort_dir = sort_dir if sort_dir is not None else ''
    if len(query) < 3:
        flash("Search Query must be at least 3 characters", "error")
        return render_template("search/search_results.html", query=query, search_type=search_type, sort_by=sort_by,
                               sort_dir=sort_dir, results=[])
    results = []
    if search_type == '':

        user_results = User.query.whooshee_search(
            query, order_by_relevance=0).all()
        preference_results = Seeking.query.whooshee_search(
            query, order_by_relevance=0).all()

        user_results_count = User.query.whooshee_search(
            query, order_by_relevance=0).count()
        preference_results_count = Seeking.query.whooshee_search(
            query, order_by_relevance=0).count()
        all_results = preference_results + user_results
        all_count = preference_results_count + user_results_count
        results = sorted(all_results)
        results.reverse()
        results = results[(page-1)*40:page*40]
        if len(results) > 0:
            paginator = QueryPagination(items=results, page=page,
                                        per_page=40, query=None, total=all_count)
            results = paginator
        else:
            results = []
    elif search_type == 'people':
        results = User.query.whooshee_search(
            query, order_by_relevance=-1).paginate(page, per_page=40)

    elif search_type == 'preference':
        results = Seeking.query.whooshee_search(
            query, order_by_relevance=-1).paginate(page, per_page=40)

    return render_template("search/search_results.html", query=query, search_type=search_type, sort_by=sort_by,
                           sort_dir=sort_dir, results=results)
