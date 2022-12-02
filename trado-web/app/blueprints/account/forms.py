from flask import url_for
from flask_wtf import FlaskForm  # ignore
from wtforms import ValidationError  # ignore
from wtforms.fields import EmailField  # ignore
from wtforms.fields import (BooleanField, PasswordField, SelectField,
                            StringField, SubmitField, TextAreaField)
from wtforms.validators import InputRequired  # ignore
from wtforms.validators import Email, EqualTo, Length, ValidationError

from app.models import User


class PrivacyForm(FlaskForm):
    is_public = SelectField(
        ' Hide from external search engines and non-registered users?', choices=[('Yes', 'Yes'), ('No', 'No')])
    hide_profile = SelectField(' Hide profile from everyone? ', choices=[
                               ('Yes', 'Yes'), ('No', 'No')])


class LoginForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):

    # , Unique(User.username)])
    username = StringField('Unique username', validators=[InputRequired()])

    #Length(1, 64),
    # Username()])
    # Unique(User.username)])

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'Username not available. Choose another username')

    first_name = StringField('First name',
                             validators=[InputRequired(),
                                         Length(1, 64)])
    last_name = StringField('Last name',
                            validators=[InputRequired(),
                                        Length(1, 64)])
    email = EmailField('Email',
                       validators=[InputRequired(),
                                   Length(1, 64),
                                   Email()])
    sex = SelectField('Gender', choices=[
                      ('Male', 'Male'), ('Female', 'Female')])
    age = SelectField(u'Select Age',
                      choices=[('18', '18'), ('19', '19'), ('20', '20'),
                               ('21', '21'), ('22', '22'), ('23', '23'),
                               ('24', '24'), ('25', '25'), ('26', '26'),
                               ('27', '27'), ('28', '28'), ('29', '29'),
                               ('30', '30'), ('31', '31'), ('32', '32'),
                               ('33', '33'), ('34', '34'), ('35', '35'),
                               ('36', '36'), ('37', '37'), ('38', '38'),
                               ('39', '39'), ('40', '40'), ('41', '41'),
                               ('42', '42'), ('43', '43'), ('44', '44'),
                               ('45', '45'), ('46', '46'), ('47', '47'),
                               ('48', '48'), ('49', '49'), ('50', '50'),
                               ('51', '51'), ('52', '52'), ('53', '53'),
                               ('54', '54'), ('55', '55'), ('56', '56'),
                               ('57', '57'), ('58', '58'), ('59', '59'),
                               ('60', '60'), ('61', '61'), ('62', '62'),
                               ('63', '63'), ('64', '64'), ('65', '65'),
                               ('66', '66'), ('67', '67'), ('68', '68'),
                               ('69', '69'), ('70', '70'), ('71', '71'),
                               ('72', '72'), ('73', '73'), ('74', '74'),
                               ('75', '75'), ('76', '76'), ('77', '77'),
                               ('78', '78'), ('79', '79'), ('80', '80'),
                               ('81', '81'), ('82', '82'), ('83', '83'),
                               ('84', '84'), ('85', '85'), ('86', '86'),
                               ('87', '87'), ('88', '88'), ('89', '89'),
                               ('90', '90'), ('91', '91'), ('92', '92'),
                               ('93', '93'), ('94', '94'), ('95', '95'),
                               ('96', '96'), ('97', '97'), ('98', '98'),
                               ('99', '99'), ('100', '100')])

    current_status = SelectField(
        ' Are you single? Married, Seperated or Widowed?',
        choices=[('Married', 'Married'), ('Seperated', 'Seperated'),
                 ('Single', 'Single'),
                 ('Single but in a relationship',
                  'Single but in a relationship'), ('Widowed', 'Widowed')])

    password = PasswordField('Password',
                             validators=[
                                 InputRequired(),
                                 EqualTo('password2', 'Passwords must match')
                             ])
    password2 = PasswordField('Confirm password', validators=[InputRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered. (Did you mean to '
                                  '<a href="{}">log in</a> instead?)'.format(
                                      url_for('account.login')))


class UpdateDetailsForm(FlaskForm):

    first_name = StringField(
        'First name', validators=[InputRequired(),
                                  Length(1, 64)])
    last_name = StringField(
        'Last name', validators=[InputRequired(),
                                 Length(1, 64)])
    city = StringField(
        'Your city', validators=[InputRequired(),
                                 Length(1, 64)])
    about = TextAreaField("TextArea", default="please add content")

    height = SelectField(' Your height ', choices=[
        ('4 feet', '4 feet'),
        ('4 feet 1 inches', '4 feet 1 inches'),
        ('4 feet 2 inches', '4 feet 2 inches'),
        ('4 feet 3 inches', '4 feet 3 inches'),
        ('4 feet 4 inches', '4 feet 4 inches'),
        ('4 feet 5 inches', '4 feet 5 inches'),
        ('4 feet 6 inches', '4 feet 6 inches'),
        ('4 feet 7 inches', '4 feet 7 inches'),
        ('4 feet 8 inches', '4 feet 8 inches'),
        ('4 feet 9 inches', '4 feet 9 inches'),
        ('4 feet 10 inches', '4 feet 10 inches'),
        ('4 feet 11 inches', '4 feet 11 inches'),
        ('5 feet', '5 feet'),
        ('5 feet 1 inches', '5 feet 1 inches'),
        ('5 feet 2 inches', '5 feet 2 inches'),
        ('5 feet 3 inches', '5 feet 3 inches'),
        ('5 feet 4 inches', '5 feet 4 inches'),
        ('5 feet 5 inches', '5 feet 5 inches'),
        ('5 feet 6 inches', '5 feet 6 inches'),
        ('5 feet 7 inches', '5 feet 7 inches'),
        ('5 feet 8 inches', '5 feet 8 inches'),
        ('5 feet 9 inches', '5 feet 9 inches'),
        ('5 feet 10 inches', '5 feet 10 inches'),
        ('5 feet 11 inches', '5 feet 11 inches'),
        ('6 feet', '6 feet'),
        ('6 feet 1 inches', '6 feet 1 inches'),
        ('6 feet 2 inches', '6 feet 2 inches'),
        ('6 feet 3 inches', '6 feet 3 inches'),
        ('6 feet 4 inches', '6 feet 4 inches'),
        ('6 feet 5 inches', '6 feet 5 inches'),
        ('6 feet 6 inches', '6 feet 6 inches'),
        ('6 feet 7 inches', '6 feet 7 inches'),
        ('6 feet 8 inches', '6 feet 8 inches'),
        ('6 feet 9 inches', '6 feet 9 inches'),
        ('6 feet 10 inches', '6 feet 10 inches'),
        ('6 feet 11 inches', '6 feet 11 inches'),
        ('7 feet', '7 feet'),
        ('7 feet 1 inches', '7 feet 1 inches'),
        ('7 feet 2 inches', '7 feet 2 inches'),
        ('7 feet 3 inches', '7 feet 3 inches'),
        ('7 feet 4 inches', '7 feet 4 inches'),
        ('7 feet 5 inches', '7 feet 5 inches'),
        ('7 feet 6 inches', '7 feet 6 inches'),
        ('7 feet 7 inches', '7 feet 7 inches'),
        ('7 feet 8 inches', '7 feet 8 inches'),
        ('7 feet 9 inches', '7 feet 9 inches'),
        ('7 feet 10 inches', '7 feet 10 inches'),
        ('7 feet 11 inches', '7 feet 11 inches'),
        ('8 feet', '8 feet')])

    sex = SelectField(' Sex', choices=[
        ('Male', 'Male'), ('Female', 'Female')])

    looking_for = SelectField(' Looking for', choices=[
        ('Male', 'Male'), ('Female', 'Female'),
        ('Existing Family', 'Existing Family')])

    age = SelectField(u'Select Age', choices=[

        ('18', '18'),
        ('19', '19'),
        ('20', '20'),
        ('21', '21'),
        ('22', '22'),
        ('23', '23'),
        ('24', '24'),
        ('25', '25'),
        ('26', '26'),
        ('27', '27'),
        ('28', '28'),
        ('29', '29'),
        ('30', '30'),
        ('31', '31'),
        ('32', '32'),
        ('33', '33'),
        ('34', '34'),
        ('35', '35'),
        ('36', '36'),
        ('37', '37'),
        ('38', '38'),
        ('39', '39'),
        ('40', '40'),
        ('41', '41'),
        ('42', '42'),
        ('43', '43'),
        ('44', '44'),
        ('45', '45'),
        ('46', '46'),
        ('47', '47'),
        ('48', '48'),
        ('49', '49'),
        ('50', '50'),
        ('51', '51'),
        ('52', '52'),
        ('53', '53'),
        ('54', '54'),
        ('55', '55'),
        ('56', '56'),
        ('57', '57'),
        ('58', '58'),
        ('59', '59'),
        ('60', '60'),
        ('61', '61'),
        ('62', '62'),
        ('63', '63'),
        ('64', '64'),
        ('65', '65'),
        ('66', '66'),
        ('67', '67'),
        ('68', '68'),
        ('69', '69'),
        ('70', '70'),
        ('71', '71'),
        ('72', '72'),
        ('73', '73'),
        ('74', '74'),
        ('75', '75'),
        ('76', '76'),
        ('77', '77'),
        ('78', '78'),
        ('79', '79'),
        ('80', '80'),
        ('81', '81'),
        ('82', '82'),
        ('83', '83'),
        ('84', '84'),
        ('85', '85'),
        ('86', '86'),
        ('87', '87'),
        ('88', '88'),
        ('89', '89'),
        ('90', '90'),
        ('91', '91'),
        ('92', '92'),
        ('93', '93'),
        ('94', '94'),
        ('95', '95'),
        ('96', '96'),
        ('97', '97'),
        ('98', '98'),
        ('99', '99'),
        ('100', '100')])

    state = StringField(
        'Your State', validators=[InputRequired(),
                                  Length(1, 64)])

    country = SelectField(u'Select Country', choices=[

        ('Afganistan', 'Afghanistan'),
        ('Albania', 'Albania'),
        ('Algeria', 'Algeria'),
        ('American Samoa', 'American Samoa'),
        ('Andorra', 'Andorra'),
        ('Angola', 'Angola'),
        ('Anguilla', 'Anguilla'),
        ('Antigua & Barbuda', 'Antigua & Barbuda'),
        ('Argentina', 'Argentina'),
        ('Armenia', 'Armenia'),
        ('Aruba', 'Aruba'),
        ('Australia', 'Australia'),
        ('Austria', 'Austria'),
        ('Azerbaijan', 'Azerbaijan'),
        ('Bahamas', 'Bahamas'),
        ('Bahrain', 'Bahrain'),
        ('Bangladesh', 'Bangladesh'),
        ('Barbados', 'Barbados'),
        ('Belarus', 'Belarus'),
        ('Belgium', 'Belgium'),
        ('Belize', 'Belize'),
        ('Benin', 'Benin'),
        ('Bermuda', 'Bermuda'),
        ('Bhutan', 'Bhutan'),
        ('Bolivia', 'Bolivia'),
        ('Bonaire', 'Bonaire'),
        ('Bosnia & Herzegovina', 'Bosnia & Herzegovina'),
        ('Botswana', 'Botswana'),
        ('Brazil', 'Brazil'),
        ('British Indian Ocean Ter', 'British Indian Ocean Ter'),
        ('Brunei', 'Brunei'),
        ('Bulgaria', 'Bulgaria'),
        ('Burkina Faso', 'Burkina Faso'),
        ('Burundi', 'Burundi'),
        ('Cambodia', 'Cambodia'),
        ('Cameroon', 'Cameroon'),
        ('Canada', 'Canada'),
        ('Canary Islands', 'Canary Islands'),
        ('Cape Verde', 'Cape Verde'),
        ('Cayman Islands', 'Cayman Islands'),
        ('Central African Republic', 'Central African Republic'),
        ('Chad', 'Chad'),
        ('Channel Islands', 'Channel Islands'),
        ('Chile', 'Chile'),
        ('China', 'China'),
        ('Christmas Island', 'Christmas Island'),
        ('Cocos Island', 'Cocos Island'),
        ('Colombia', 'Colombia'),
        ('Comoros', 'Comoros'),
        ('Congo', 'Congo'),
        ('Cook Islands', 'Cook Islands'),
        ('Costa Rica', 'Costa Rica'),
        ('Cote DIvoire', 'Cote DIvoire'),
        ('Croatia', 'Croatia'),
        ('Cuba', 'Cuba'),
        ('Curaco', 'Curacao'),
        ('Cyprus', 'Cyprus'),
        ('Czech Republic', 'Czech Republic'),
        ('Denmark', 'Denmark'),
        ('Djibouti', 'Djibouti'),
        ('Dominica', 'Dominica'),
        ('Dominican Republic', 'Dominican Republic'),
        ('East Timor', 'East Timor'),
        ('Ecuador', 'Ecuador'),
        ('Egypt', 'Egypt'),
        ('El Salvador', 'El Salvador'),
        ('Equatorial Guinea', 'Equatorial Guinea'),
        ('Eritrea', 'Eritrea'),
        ('Estonia', 'Estonia'),
        ('Ethiopia', 'Ethiopia'),
        ('Falkland Islands', 'Falkland Islands'),
        ('Faroe Islands', 'Faroe Islands'),
        ('Fiji', 'Fiji'),
        ('Finland', 'Finland'),
        ('France', 'France'),
        ('French Guiana', 'French Guiana'),
        ('French Polynesia', 'French Polynesia'),
        ('French Southern Ter', 'French Southern Ter'),
        ('Gabon', 'Gabon'),
        ('Gambia', 'Gambia'),
        ('Georgia', 'Georgia'),
        ('Germany', 'Germany'),
        ('Ghana', 'Ghana'),
        ('Gibraltar', 'Gibraltar'),
        ('Great Britain', 'Great Britain'),
        ('Greece', 'Greece'),
        ('Greenland', 'Greenland'),
        ('Grenada', 'Grenada'),
        ('Guadeloupe', 'Guadeloupe'),
        ('Guam', 'Guam'),
        ('Guatemala', 'Guatemala'),
        ('Guinea', 'Guinea'),
        ('Guyana', 'Guyana'),
        ('Haiti', 'Haiti'),
        ('Hawaii', 'Hawaii'),
        ('Honduras', 'Honduras'),
        ('Hong Kong', 'Hong Kong'),
        ('Hungary', 'Hungary'),
        ('Iceland', 'Iceland'),
        ('Indonesia', 'Indonesia'),
        ('India', 'India'),
        ('Iran', 'Iran'),
        ('Iraq', 'Iraq'),
        ('Ireland', 'Ireland'),
        ('Isle of Man', 'Isle of Man'),
        ('Israel', 'Israel'),
        ('Italy', 'Italy'),
        ('Jamaica', 'Jamaica'),
        ('Japan', 'Japan'),
        ('Jordan', 'Jordan'),
        ('Kazakhstan', 'Kazakhstan'),
        ('Kenya', 'Kenya'),
        ('Kiribati', 'Kiribati'),
        ('Korea North', 'Korea North'),
        ('Korea Sout', 'Korea South'),
        ('Kuwait', 'Kuwait'),
        ('Kyrgyzstan', 'Kyrgyzstan'),
        ('Laos', 'Laos'),
        ('Latvia', 'Latvia'),
        ('Lebanon', 'Lebanon'),
        ('Lesotho', 'Lesotho'),
        ('Liberia', 'Liberia'),
        ('Libya', 'Libya'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Lithuania', 'Lithuania'),
        ('Luxembourg', 'Luxembourg'),
        ('Macau', 'Macau'),
        ('Macedonia', 'Macedonia'),
        ('Madagascar', 'Madagascar'),
        ('Malaysia', 'Malaysia'),
        ('Malawi', 'Malawi'),
        ('Maldives', 'Maldives'),
        ('Mali', 'Mali'),
        ('Malta', 'Malta'),
        ('Marshall Islands', 'Marshall Islands'),
        ('Martinique', 'Martinique'),
        ('Mauritania', 'Mauritania'),
        ('Mauritius', 'Mauritius'),
        ('Mayotte', 'Mayotte'),
        ('Mexico', 'Mexico'),
        ('Midway Islands', 'Midway Islands'),
        ('Moldova', 'Moldova'),
        ('Monaco', 'Monaco'),
        ('Mongolia', 'Mongolia'),
        ('Montserrat', 'Montserrat'),
        ('Morocco', 'Morocco'),
        ('Mozambique', 'Mozambique'),
        ('Myanmar', 'Myanmar'),
        ('Nambia', 'Nambia'),
        ('Nauru', 'Nauru'),
        ('Nepal', 'Nepal'),
        ('Netherland Antilles', 'Netherland Antilles'),
        ('Netherlands', 'Netherlands (Holland, Europe)'),
        ('Nevis', 'Nevis'),
        ('New Caledonia', 'New Caledonia'),
        ('New Zealand', 'New Zealand'),
        ('Nicaragua', 'Nicaragua'),
        ('Niger', 'Niger'),
        ('Nigeria', 'Nigeria'),
        ('Niue', 'Niue'),
        ('Norfolk Island', 'Norfolk Island'),
        ('Norway', 'Norway'),
        ('Oman', 'Oman'),
        ('Pakistan', 'Pakistan'),
        ('Palau Island', 'Palau Island'),
        ('Palestine', 'Palestine'),
        ('Panama', 'Panama'),
        ('Papua New Guinea', 'Papua New Guinea'),
        ('Paraguay', 'Paraguay'),
        ('Peru', 'Peru'),
        ('Phillipines', 'Philippines'),
        ('Pitcairn Island', 'Pitcairn Island'),
        ('Poland', 'Poland'),
        ('Portugal', 'Portugal'),
        ('Puerto Rico', 'Puerto Rico'),
        ('Qatar', 'Qatar'),
        ('Republic of Montenegro', 'Republic of Montenegro'),
        ('Republic of Serbia', 'Republic of Serbia'),
        ('Reunion', 'Reunion'),
        ('Romania', 'Romania'),
        ('Russia', 'Russia'),
        ('Rwanda', 'Rwanda'),
        ('St Barthelemy', 'St Barthelemy'),
        ('St Eustatius', 'St Eustatius'),
        ('St Helena', 'St Helena'),
        ('St Kitts-Nevis', 'St Kitts-Nevis'),
        ('St Lucia', 'St Lucia'),
        ('St Maarten', 'St Maarten'),
        ('St Pierre & Miquelon', 'St Pierre & Miquelon'),
        ('St Vincent & Grenadines', 'St Vincent & Grenadines'),
        ('Saipan', 'Saipan'),
        ('Samoa', 'Samoa'),
        ('Samoa American', 'Samoa American'),
        ('San Marino', 'San Marino'),
        ('Sao Tome & Principe', 'Sao Tome & Principe'),
        ('Saudi Arabia', 'Saudi Arabia'),
        ('Senegal', 'Senegal'),
        ('Seychelles', 'Seychelles'),
        ('Sierra Leone', 'Sierra Leone'),
        ('Singapore', 'Singapore'),
        ('Slovakia', 'Slovakia'),
        ('Slovenia', 'Slovenia'),
        ('Solomon Islands', 'Solomon Islands'),
        ('Somalia', 'Somalia'),
        ('South Africa', 'South Africa'),
        ('Spain', 'Spain'),
        ('Sri Lanka', 'Sri Lanka'),
        ('Sudan', 'Sudan'),
        ('Suriname', 'Suriname'),
        ('Swaziland', 'Swaziland'),
        ('Sweden', 'Sweden'),
        ('Switzerland', 'Switzerland'),
        ('Syria', 'Syria'),
        ('Tahiti', 'Tahiti'),
        ('Taiwan', 'Taiwan'),
        ('Tajikistan', 'Tajikistan'),
        ('Tanzania', 'Tanzania'),
        ('Thailand', 'Thailand'),
        ('Togo', 'Togo'),
        ('Tokelau', 'Tokelau'),
        ('Tonga', 'Tonga'),
        ('Trinidad & Tobago', 'Trinidad & Tobago'),
        ('Tunisia', 'Tunisia'),
        ('Turkey', 'Turkey'),
        ('Turkmenistan', 'Turkmenistan'),
        ('Turks & Caicos Is', 'Turks & Caicos Is'),
        ('Tuvalu', 'Tuvalu'),
        ('Uganda', 'Uganda'),
        ('United Kingdom', 'United Kingdom'),
        ('Ukraine', 'Ukraine'),
        ('United Arab Erimates', 'United Arab Emirates'),
        ('United States of America', 'United States of America'),
        ('Uraguay', 'Uruguay'),
        ('Uzbekistan', 'Uzbekistan'),
        ('Vanuatu', 'Vanuatu'),
        ('Vatican City State', 'Vatican City State'),
        ('Venezuela', 'Venezuela'),
        ('Vietnam', 'Vietnam'),
        ('Virgin Islands (Brit)', 'Virgin Islands (Brit)'),
        ('Virgin Islands (USA)', 'Virgin Islands (USA)'),
        ('Wake Island', 'Wake Island'),
        ('Wallis & Futana Is', 'Wallis & Futana Is'),
        ('Yemen', 'Yemen'),
        ('Zaire', 'Zaire'),
        ('Zambia', 'Zambia'),
        ('Zimbabwe', 'Zimbabwe')])

    religion = SelectField(' Select your religion', choices=[
        ('Christianity', 'Christianity'),
        ('Judaism', 'Judaism'),
        ('Islam', 'Islam'),
        ('Hinduism', 'Hinduism'),
        ('None', 'None'),
        ('Others', 'Others')])

    ethnicity = SelectField(' Select your ethnicity', choices=[
        ('African American', 'African American'),
        ('Caucasian', 'Caucasian'),
        ('European', 'European'),
        ('Hispanic', 'Hispanic'),
        ('Indian', 'Indian'),
        ('Middle Eastern', 'Middle Eastern'),
        ('African', 'African'),
        ('Native American (Indian)', 'Native American (Indian)'),
        ('Asian', 'Asian'),
        ('Pacific Islander', 'Pacific Islander'),
        ('Caribbean', 'Caribbean'),
        ('Mixed Race', 'Mixed Race'),
        ('Other Ethnicity', 'Other Ethnicity')
    ])

    marital_type = SelectField(' Relationship Preference', choices=[
        ('Monogamy', 'Monogamy'),
        ('Polygamy', 'Polygamy'),
        ('Both Polygamy or Monogamy', 'Both Polygamy or Monogamy')])

    body_type = SelectField(' Select Body type', choices=[
        ('Slender', 'Slender'),
        ('Athletic', 'Athletic'),
        ('Average', 'Average'),
        ('A Few Extra Pounds', 'A Few Extra Pounds'),
        ('Big & Tall/BBW', 'Big & Tall/BBW'),
        ('Muscular', 'Muscular'),

        ('Voluptuous', 'Voluptuous'),
        ('Petite', 'Petite'),
        ('Well Proportioned', 'Well Proportioned'),
        ('Curvy/Curvaceous', 'Curvy/Curvaceous'),
    ])

    church_denomination = SelectField(' Select Christian Denomination', choices=[
        ('7th Day Adventist', '7th Day Adventist'),
        ('Anglican', 'Anglican'),
        ('Apostolic Assembly of God', 'Apostolic Assembly of God'),
        ('Baptist', 'Baptist'),
        ('Catholic', 'Catholic'),
        ('Charismatic', 'Charismatic'),

        ('Christian Reformed', 'Christian Reformed'),
        ('Church of Christ', 'Church of Christ'),
        ('Church of God', 'Church of God'),
        ('Episcopalian', 'Episcopalian'),
        ('Evangelical', 'Evangelical'),

        ('Interdenominational', 'Interdenominational'),
        ('Lutheran', 'Lutheran'),
        ('Mennonite', 'Mennonite'),
        ('Messianic', 'Messianic'),

        ('Methodist', 'Methodist'),
        ('Missionary Alliance', 'Missionary Alliance'),
        ('Nazarene', 'Nazarene'),
        ('Non-Denominational', 'Non-Denominational'),

        ('Orthodox', 'Orthodox'),
        ('Pentecostal', 'Pentecostal'),
        ('Presbyterian', 'Presbyterian'),
        ('Protestant', 'Protestant'),

        ('Reformed', 'Reformed'),
        ('Southern Baptist', 'Southern Baptist'),
        ('United', 'United'),
        ('United Pentecostal Church', 'United Pentecostal Church'),
        ('Jehovah Withness', 'Jehovah Withness'),
        ('Other', 'Other')
    ])

    current_status = SelectField(' Are you single? Married, Seperated or Widowed?', choices=[
        ('Married', 'Married'),
        ('Seperated', 'Seperated'),
        ('Single', 'Single'),
        ('Single but in a relationship', 'Single but in a relationship'),
        ('Widowed', 'Widowed')])

    drinking_status = SelectField(' Do you drink?', choices=[
        ('No', 'No'),
        ('Socially', 'Socially'),
        ('Ocassionally', 'Ocassionally'),
        ('Frequently', 'Frequently'),
        ('Daily', 'Daily')])

    smoking_status = SelectField(' Do you smoke?', choices=[
        ('No', 'No'),
        ('Socially', 'Socially'),
        ('Ocassionally', 'Ocassionally'),
        ('Frequently', 'Frequently'),
        ('Daily', 'Daily')])

    education_level = SelectField('Education Level', choices=[
        ('Some School', 'Some School'),
        ('GED', 'GED'),
        ('High School Graduate', 'High School Graduate'),
        ('Specialty/Trade School', 'Specialty/Trade School'),
        ('Some College', 'Some College'),

        ('2 Yr College Degree/Diploma', '2 Yr College Degree/Diploma'),
        ('4 Yr College Degree/Diploma', '4 Yr College Degree/Diploma'),
        ('Masters/Post Graduate Diploma', 'Masters/Post Graduate Diploma'),

        ('Ph.D./Doctorate', 'Ph.D./Doctorate')])

    has_children = SelectField(' Do you have kids?', choices=[
        ('Yes', 'Yes'),
        ('Yes but all grown', 'Yes but all grown'),
        ('No', 'No')])

    want_children = SelectField(' Do you want kids?', choices=[
        ('Yes', 'Yes'),
        ('Does Not Want Children', 'Does Not Want Children'),
        ('Undecided/Open', 'Undecided/Open')])

    open_for_relocation = SelectField(' Would you be willing to relocate ?', choices=[
        ('Yes', 'Yes'),
        ('Maybe ', 'Maybe'),
        ('No', 'No')])


class RequestResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])

    # We don't validate the email address so we don't confirm to attackers
    # that an account with the given email exists.


class ResetPasswordForm(FlaskForm):
    email = EmailField(
        'Email', validators=[InputRequired(),
                             Length(1, 64),
                             Email()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Unknown email address.')


class CreatePasswordForm(FlaskForm):
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('password2', 'Passwords must match.')
        ])
    password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old password', validators=[InputRequired()])
    new_password = PasswordField(
        'New password',
        validators=[
            InputRequired(),
            EqualTo('new_password2', 'Passwords must match.')
        ])
    new_password2 = PasswordField(
        'Confirm new password', validators=[InputRequired()])


class ChangeEmailForm(FlaskForm):
    email = EmailField(
        'New email', validators=[InputRequired(),
                                 Length(1, 64),
                                 Email()])
    password = PasswordField('Password', validators=[InputRequired()])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')


class ChangeUsernameForm(FlaskForm):
    username = StringField(
        'New username', validators=[InputRequired(),
                                    Length(1, 64)])
    password = PasswordField('Password', validators=[InputRequired()])

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(
                'Username already exist, try a different one.')
