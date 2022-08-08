from flask import Blueprint, render_template

from app.models import *

public = Blueprint('public', __name__)


@public.route('/')
def index():
    """Home page for the website"""

    nav_menu = NavMenu.query.all()
    slideshows = SlideShowImage.query.all()
    hometext = HomeText.query.first()
    call_to_action = CallToAction.query.all()
    logo = Logo.query.first()
    techno_img = TechnologiesImage.query.all()
    text_techno = TechnologiesText.query.first()
    footer_text = FooterText.query.all()
    tracking_script = TrackingScript.query.all()
    media_icons = SocialMediaIcon.query.all()
    footer_image = FooterImage.query.first()
    copyright_text = CopyRight.query.first()
    background_image = BackgroundImage.query.first()
    favicon_image = FaviconImage.query.first()
    brand = BrandName.query.first()
    seo = Seo.query.first()
    services = Service.query.all()
    about = About.query.first()
    team = Team.query.all()
    video = Video.query.first()
    counts = Counter.query.all()
    portfolio = Portfolio.query.all()
    faq = Faq.query.all()
    testimonial = Testimonial.query.all()
    client = Client.query.all()
    apple_touch_icon = AppleTouchIcon.query.first()
    pages = Page.query.all()
    features = Feature.query.all()
    feature_title = FeatureTitle.query.first()
    process_title = ProcessTitle.query.first()
    process = Process.query.all()
    landing_page_texts = LandingPageText.query.all()
    video_texts = VideoText.query.first()
    
    return render_template('public/index.html', video_texts=video_texts, landing_page_texts=landing_page_texts,
                           process_title=process_title, process=process,
                           features=features, feature_title = feature_title,
                           footer_image=footer_image, icons=media_icons,
                           footer_text=footer_text, slideshows=slideshows,
                           home_title=hometext, logo=logo, techno_img=techno_img,
                           text_techno=text_techno, copyright_text=copyright_text,
                           background_image=background_image, call_to_action=call_to_action,
                           nav_menu=nav_menu, brand=brand, seo=seo,
                           favicon_image=favicon_image, tracking_script=tracking_script, services=services,
                           about=about, team=team, video=video, counts=counts, media_icons = media_icons,
                           portfolio=portfolio, faq=faq, testimonial=testimonial, client=client,
                           apple_touch_icon=apple_touch_icon, pages=pages)


@public.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'public/about.html', editable_html_obj=editable_html_obj)
