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
from flask_rq import get_queue
from flask_ckeditor import upload_success
from flask_sqlalchemy import Pagination
from sqlalchemy import desc, func
import operator


from app import db
#from app.page_manager.forms import (
    #ChangeAccountTypeForm,
    #ChangeUserEmailForm,
    #InviteUserForm,
    #NewUserForm,
#)
from app.decorators import admin_required
from app.email import send_email
from app.models import *
from app.blueprints.search.forms import *

search = Blueprint('search', __name__)



@search.route('/test')
def test():
    test_search = User.query.whooshee_search('Shawn').order_by(User.id.desc()).first()
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
        
        user_results = User.query.whooshee_search(query, order_by_relevance=0).all()
        preference_results = Seeking.query.whooshee_search(query, order_by_relevance=0).all()
##        questions_results = Question.query.whooshee_search(query, order_by_relevance=0).all()
        #products_results = MProduct.query.whooshee_search(query).all()

        user_results_count = User.query.whooshee_search(query, order_by_relevance=0).count()
        preference_results_count = Seeking.query.whooshee_search(query, order_by_relevance=0).count()
##        questions_results_count = Question.query.whooshee_search(query, order_by_relevance=0).count()
##        products_results_count = MProduct.query.whooshee_search(query, order_by_relevance=0).count()

        all_results = preference_results + user_results
        all_count = preference_results_count + user_results_count
        results = sorted(all_results)
        results.reverse()
        results = results[(page-1)*40:page*40]
        paginator = Pagination(items=results, page=page, per_page=40, query=None, total=all_count)
        results = paginator

    elif search_type == 'people':
        people_results = User.query.whooshee_search(query, order_by_relevance=-1).paginate(page, per_page=40)
        #results = sorted(user_results, key=operator.attrgetter("score"))
##    elif search_type == 'jobs':
##        results = Job.query.whooshee_search(query, order_by_relevance=-1).paginate(page, per_page=40)
##        # results = sorted(job_results, key=operator.attrgetter("score"))
##    elif search_type == 'questions':
##        results = Question.query.whooshee_search(query, order_by_relevance=-1).paginate(page, per_page=40)
##        # results = sorted(questions_results, key=operator.attrgetter("score"))   
##    elif search_type == 'products':
##        results = MProduct.query.whooshee_search(query, order_by_relevance=10).paginate(page, per_page=8)
        # results = sorted(products_results, key=operator.attrgetter("score"))

    elif search_type == 'preference':
        preference_results = Seeking.query.whooshee_search(query, order_by_relevance=-1).paginate(page, per_page=40)
        #results = sorted(preference_results, key=operator.attrgetter("score"))

    
    return render_template("search/search_results.html", query=query, search_type=search_type, sort_by=sort_by,
                           sort_dir=sort_dir, results=results,
                           preference_results=preference_results,
                           people_results=people_results,
                           user_results=user_results)
