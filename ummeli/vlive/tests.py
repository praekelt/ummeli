from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import mail

from ummeli.vlive.utils import render_to_pdf
from ummeli.api.models import Certificate
from ummeli.vlive.models import Province,  Article,  Category
from ummeli.vlive.jobs_util import CategoryParser,  JobsParser

import json
import urllib

class VliveTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
    
    def tearDown(self):
        pass
        
    def test_index_page(self):
        username = 'user'
        password = 'password'
        user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username=username, password=password)
        resp = self.client.get(reverse('index'))
         #  there shouldn't be a Location header as this would mean a redirect
         #  to a login URL
        self.assertEquals(resp.get('Location', None), None)
        self.assertEquals(resp.status_code, 200)
        
    def test_login_view(self):
        msisdn = '0123456789'
        password = 'password'
        user = User.objects.create_user(msisdn, '%s@domain.com' % msisdn, 
                                        password)
        resp = self.client.get(reverse('login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get(reverse('login'), 
                                {'username': msisdn, 'password': password, 
                                '_action': 'POST'}, 
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
                                
        self.assertEquals(resp.status_code, 200)  # redirect to index
        self.assertContains(resp, 'Edit CV')
        
        resp = self.client.get(reverse('login'), 
                               {'password': 'wrong_pin', '_action': 'POST'},
                                HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        self.assertEquals(resp.status_code, 200)      
        self.assertContains(resp, 'Sign in failed')

    def test_basic_registration_flow(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.get(reverse('index'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        #self.assertEquals(resp.status_code, 302)  # redirect to login
        #self.assertEquals(resp.get('Location', None), 
        #                'http://testserver/vlive/login?next=/vlive/')
        
        resp = self.client.get(reverse('login'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Click here to create profile.')
        
        resp = self.client.get(reverse('register'), HTTP_X_UP_CALLING_LINE_ID=msisdn)
        self.assertEquals(resp.status_code, 200)
        
        self.assertContains(resp, 'Create pin for %s' % (msisdn))
        
        resp = self.client.get(reverse('register'),
                                {'username': msisdn, 'password1': password, 
                                'password2': password,  '_action': 'POST'},  
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Enter Pin to sign in.')
        
        resp = self.client.get(reverse('login'), 
                                {'username': msisdn, 'password': password, 
                                '_action': 'POST'}, 
                                HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Edit CV')

    def test_registration_invalid_pin(self):
        msisdn = '0123456789'
        password = 'password'
        
        resp = self.client.get(reverse('register'), 
                               {'username': msisdn, 'password1': password, 
                               'password2': 'wrong',  '_action': 'POST'}, 
                               HTTP_X_UP_CALLING_LINE_ID = msisdn, )
        print resp
        self.assertContains(resp, 'Pin codes don&apos;t match.')
        
class JobsTestCase(TestCase):
    
    def test_job_models(self):
        province = Province.objects.create(search_id = 1,  name='Gauteng')        
        cat = Category.objects.create(title='Domestic')
        province.job_categories.add(cat)
        
        cat = Category.objects.create(title='Domestic')
        
        self.assertEquals(Province.objects.count(),  1)
        self.assertEquals(len(province.job_categories.all()),  1)
        
        province.job_categories.clear()
        self.assertEquals(len(province.job_categories.all()),  0)
        self.assertEquals(Province.objects.count(),  1)
        
    def test_category_parser(self):
        html = """
        <a name="top"></a>
<center><img src="/branding/iol/images/wegotads-logo.png" width="260" height="43" alt="WeGotAds South Africa"></center>		
		<!-- start contents --> 
		<div id="thecontent"> 
				<!--  breadcrumb --> 
				<div style="background-color:silver;border-top:1px solid black;border-bottom:2px solid black;" id="breadcrumb" class="breadcrumb">
				<font size=14><a href="http://www.wegotads.co.za/bluefin.cmp?&sfid=1" class="breadcrumbNavigation">Classifieds</a> &raquo; <a href="Employment/listings/22001" class="breadcrumbNavigation">Employment</a> &raquo; <a href="Accounts%2FFinancial/listings/601" class="breadcrumbNavigation">Accounts/Financial</a></font>				</div> 
		<div align="center">
<br>
<form action="http://www.wegotads.co.za/advanced_search_result.cmp"  accept-charset="UTF-8" method="get" id="quick_find"> 
<input type=hidden id="sfid" name="sfid" value="1">
<input type=hidden id="search_source" name="search_source" value="1">
<div class="form-item"> 
<input style="width:400px;height:40px;font-size:24pt;" type="text" name="keywords" id="keywords"  size="40" value="" class="form-text required" /> 
<span id="search_region_field"><select style="height:40px;font-size:24pt;" name="search_source"><option selected="selected" value="1">All of South Africa</option><option value="">----------------</option><option value="2">Gauteng</option><option value="9">---&nbsp;The Star</option><option value="5">Western Cape</option><option value="12">---&nbsp;The Argus</option><option value="6">KZN</option><option value="15">---&nbsp;Mercury</option></select></span>
 <input style="font-size:24pt;height:40;" type=submit value="Search">
 </div> 
</form>
</div>		 
		 <form name="marketplace" id="marketplace" action="http://www.wegotads.co.za/bluefin.cmp?&sfid=1" method="get"><input type="hidden" name="action" id="action" value="process"><input type="hidden" name="cPath" id="cPath" value="601"><input type="hidden" name="bfcid" id="bfcid" value="aigaaoid5pg8djla4sfd7vm854"><input type="hidden" name="product_filter" id="product_filter" value="all"><input type="hidden" name="sfid" id="sfid" value="1"></form							
		    <div id="topright">
		        <h1></h1>
		    </div>
		                    <div class="category">
		<table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font></td><td valign="top" style="padding-left:10px;"><font size=14>A Career in
Accounts Admin
Your quickest way to a job. Our 2 month course covering Manual Bookkeeping ACCPAC / Email /PASTEL Manual wages/Vip Payroll/ MS Excel & free CV/ job assistance.
ACCPAC/PASTEL
www.cadtraining.co.za
C.A.D. Training Centre
Ph 418 1455/ 419 8977</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font></td><td valign="top" style="padding-left:10px;"><font size=14>A leading company in the Travel Industry has recently required the services in their financial department :
? Financial Accountant Perm R15-20k
? Internal Auditor Contract R15-20k
? Reconciliation Expert Perm R10k
? Junior Accountant Temp R5-10k
? Debtors Manager Perm R15-20k
? Salaries Clerk (VIP Payroll) Perm R7 -9k
Email CV to:
hr@gtasa.co.za
with reference to position you are applying for.</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Gauteng</font><br/><a href="//images/upload/8439966.jpg"><img width="200" class="logo_size" src=//images/upload/8439966.jpg alt="" width=70 align=right border=0></td><td valign="top" style="padding-left:10px;"><font size=14>Accounting  &
Pastel  Course
Full  Time
10  -  20  Oct
Part  Time
8  Oct  - 3  Dec
Only  12  per  class
Accredited  ATC
(011) 622 5158
072 894 7536
questcomputerskills.co.za</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font><br/><a href="//images/upload/8444851.jpg"><img width="200" class="logo_size" src=//images/upload/8444851.jpg alt="" width=70 align=right border=0></td><td valign="top" style="padding-left:10px;"><font size=14>Accounts Payable Manager
Opportunity for Graduate with 3 years solid accounts payable/management experience to lead a team in highly professional/corporate environment. R350 000 CTC. eMail CV; copy of degree; payslip to: lorna@obr.co.za</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font><br/><a href="//images/upload/8443367.jpg"><img width="200" class="logo_size" src=//images/upload/8443367.jpg alt="" width=70 align=right border=0></td><td valign="top" style="padding-left:10px;"><font size=14>Accounts Payable Team Leader - CBD
R30k
Africa's largest law firm is looking for your prev exp as an Accounts Payable Team Leader. Your duties will include managing a large team. Your relevant qualification is essential. Plse forward your CV to lindie@obr.co.za.</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Gauteng</font></td><td valign="top" style="padding-left:10px;"><font size=14>BOKSBURG BASED SECURITY COMPANY REQUIRES THE SERVICES OF A FINANCIAL ADMINISTRATOR
Minimum requirement National Diploma in Accounting. 3 yrs experience. Microsoft Word, Powerpoint and Exel. Bookkeeping experience essential. If you meet the above requirements E-mail your detailed CV and certified copies of all qualifications TO nombulelo@gbrtsecurity.co.za or fax to 0866231421.</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font><br/><a href="//images/upload/8443122.jpg"><img width="200" class="logo_size" src=//images/upload/8443122.jpg alt="" width=70 align=right border=0></td><td valign="top" style="padding-left:10px;"><font size=14>Bookkeeper
5 month contract, R10 000, C City 
Do you know Pastel, Quickbooks or MYOB? Can you commence duties on 1 November 2011? Do you have experience working with multiple sets of books? Experience working to Trial Balance but with exposure to Balance Sheet. Ability to learn quickly, multitask and think on your feet essential. Own car also essential. Please email your CV to lesley@obr.co.za quoting position in the subject heading.</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font><br/><a href="//images/upload/8445343.jpg"><img width="200" class="logo_size" src=//images/upload/8445343.jpg alt="" width=70 align=right border=0></td><td valign="top" style="padding-left:10px;"><font size=14>CR's CLERK
Use your strong CR's exp to extend your career with our Large Int Imports Co, req min 3yr exp, Immd Avail or max 2 wks notice. R10-12k. View job spec www.timepersonnel.co.za Email caroline@timepersonnel.co.za</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font><br/><a href="//images/upload/8443112.jpg"><img width="200" class="logo_size" src=//images/upload/8443112.jpg alt="" width=70 align=right border=0></td><td valign="top" style="padding-left:10px;"><font size=14>Creditor's/Accounts Clerk
R8 000 neg + benefits, Hout Bay
Do you have 2 years' experience in Creditors and Accounts? Do you reside near to Hout Bay? Do you have experience in petty cash and asset registers? Are you flexible and quick to learn? Do you know Pastel? This international concern is looking for someone with all of the above! Please email your CV to: lesley@obr.co.za (Creditor's Clerk in the subject heading).</font></td></tr><table style="border-bottom:1px solid silver;"><tr><td width=200 valign="top" style="padding-right:10px;border-right:1px solid silver;"><font size=14>03-10</font><font color=silver size=14><br/>Western Cape</font><br/><a href="//images/upload/8445206.jpg"><img width="200" class="logo_size" src=//images/upload/8445206.jpg alt="" width=70 align=right border=0></td><td valign="top" style="padding-left:10px;"><font size=14>Creditors/Accounts Clerk
Houtbay
? Matric
? 2-3 yrs exp
? Pastel V9-10 ess.
? Processing of Creditors on Pastel
? Accounting principles, asset register and petty cash knowledge
Contact Shahieda (021) 910 6221</font></td></tr></table><center><div class="page"><font size=14>&nbsp;Page&nbsp;1&nbsp;of&nbsp;24&nbsp;&nbsp;<a  href="Accounts%2FFinancial/listings/601-2?umb=1&search_source=1" title="Next">Next &#62;&#62;</a></font></div></center>		           		    		    
		</div> 		
		<br/><br/>
		<center><a href="http://www.wegotads.co.za/bluefin.cmp?umb=0&sfid=1">Full Web Site</a>&nbsp;&nbsp;|&nbsp;&nbsp;
<a href="javascript://" onClick="location.hash='top'">Top of Page</a>
</center><center>Copyright 2011 - Independent Newspapers. All Rights Reserved.</center>		
</body></html>"""
        parser = JobsParser(html_str = html)
        items = parser.parse()
        
        self.assertEquals(len(items),  10)
        
class VliveCVTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        username = 'user'
        password = 'password'
        self.user = User.objects.create_user(username, '%s@domain.com' % username, 
                                        password)
        self.client.login(username=username, password=password)
    
    def tearDown(self):
        pass
        
    def test_edit_personal_page(self):
        msisdn = '0123456789'
        
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('edit'), 
                                        'personal'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'firstName': 'Milton', 'gender': 'Male',  
                        '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        cv = self.user.get_profile()
        self.assertEquals(cv.firstName, 'Milton')
        self.assertEquals(cv.gender, 'Male')
            
    def test_edit_contact_details_page(self):
        msisdn = '0123456789'
        
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('edit'), 
                                        'contact'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'telephoneNumber': '0123456978', 'streetName': 'Oak Rd', 
                     '_action': 'POST'}
        resp = self.client.get(reverse('edit_contact'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        cv = self.user.get_profile()
        self.assertEquals(cv.telephoneNumber, '0123456978')
        self.assertEquals(cv.streetName, 'Oak Rd')
        
    def test_edit_education_details_page(self):
        msisdn = '0123456789'
        
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('edit'), 
                                        'education'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'highestGrade': '12', 'highestGradeYear': 2005,
                    'school': 'Some school',  '_action': 'POST'}
        resp = self.client.get(reverse('edit_education'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
        
        cv = self.user.get_profile()
        self.assertEquals(cv.highestGrade, '12')
        self.assertEquals(cv.highestGradeYear, 2005)
        self.assertEquals(cv.school, 'Some school')

    def test_edit_certificates_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates listing
        resp = self.client.get(reverse('certificate_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add form
        resp = self.client.get(reverse('certificate_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add action
        post_data = {'name': 'BSc', 'institution': 'UCT', 'year': 2007}
        resp = self.client.post(reverse('certificate_new'),  post_data)
        
         # test certificates listing of new certificate
        resp = self.client.get(reverse('certificate_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'BSc')
        
         # test editing of created certificate
        resp = self.client.get(reverse('certificate_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'name': 'BSc in IT', 'institution': 'UCT', 'year': 2007}
        resp = self.client.post(reverse('certificate_edit', args=[1]),  
                                post_data)
        
        resp = self.client.get(reverse('certificate_list'))
        self.assertContains(resp, 'BSc in IT')
        
        certs = self.user.get_profile().certificates
        self.assertEquals(len(certs.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('certificate_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('certificate_delete',  args=[1]))
        certs = self.user.get_profile().certificates
        self.assertEquals(len(certs.all()), 0)        

    def test_edit_workExperiences_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates listing
        resp = self.client.get(reverse('workExperience_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add form
        resp = self.client.get(reverse('workExperience_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test certificates add action
        post_data = {'title': 'Engineer', 'company': 'Praekelt', 
                    'startYear': 2007, 'endYear': 2008}
        resp = self.client.post(reverse('workExperience_new'),  post_data)
        
         # test certificates listing of new certificate
        resp = self.client.get(reverse('workExperience_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Praekelt')
        
         # test editing of created certificate
        resp = self.client.get(reverse('workExperience_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'title': 'Engineer', 'company': 'Praekelt Consulting', 
                    'startYear': 2007, 'endYear': 2008}
        resp = self.client.post(reverse('workExperience_edit', args=[1]),  
                                post_data)
        print resp
        resp = self.client.get(reverse('workExperience_list'))
        self.assertContains(resp, 'Praekelt Consulting')
        
        workExperiences = self.user.get_profile().workExperiences
        self.assertEquals(len(workExperiences.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('workExperience_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('workExperience_delete',  args=[1]))
        workExperiences = self.user.get_profile().workExperiences
        self.assertEquals(len(workExperiences.all()), 0)
        
    def test_edit_languages_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test languages listing
        resp = self.client.get(reverse('language_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test language add form
        resp = self.client.get(reverse('language_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test languageadd action
        post_data = {'language': 'English', 'readWrite': True}
        resp = self.client.post(reverse('language_new'),  post_data)
        
         # test listing of new language
        resp = self.client.get(reverse('language_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'English')
        
         # test editing of created certificate
        resp = self.client.get(reverse('language_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'language': 'Afrikaans', 'readWrite': True}
        resp = self.client.post(reverse('language_edit', args=[1]),  
                                post_data)
        
        resp = self.client.get(reverse('language_list'))
        self.assertContains(resp, 'Afrikaans')
        
        languages = self.user.get_profile().languages
        self.assertEquals(len(languages.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('language_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('language_delete',  args=[1]))
        languages = self.user.get_profile().languages
        self.assertEquals(len(languages.all()), 0)        
        
    def test_edit_references_details_page(self):
        resp = self.client.get(reverse('edit'))
        self.assertEquals(resp.status_code, 200)
        
         # test references listing
        resp = self.client.get(reverse('reference_list'))
        self.assertEquals(resp.status_code, 200)
        
         # test reference add form
        resp = self.client.get(reverse('reference_new'))
        self.assertEquals(resp.status_code, 200)
        
         # test reference add action
        post_data = {'fullname': 'Test', 'relationship': 'Manager'}
        resp = self.client.post(reverse('reference_new'),  post_data)
        
         # test listing of new reference
        resp = self.client.get(reverse('reference_list'))        
        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, 'Test')
        
         # test editing of created reference
        resp = self.client.get(reverse('reference_edit',  args=[1]))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'fullname': 'User', 'relationship': 'Manager'}
        resp = self.client.post(reverse('reference_edit', args=[1]),  
                                post_data)
        
        resp = self.client.get(reverse('reference_list'))
        self.assertContains(resp, 'User')
        
        references = self.user.get_profile().references
        self.assertEquals(len(references.all()), 1)
        
         # test delete action
        resp = self.client.get(reverse('reference_delete',  args=[1]))
        self.assertContains(resp, 'Are you sure')
        
        resp = self.client.post(reverse('reference_delete',  args=[1]))
        references = self.user.get_profile().references
        self.assertEquals(len(references.all()), 0)                
        
    def test_convert_to_pdf(self):
        cv = self.user.get_profile()
        result = render_to_pdf('vlive/pdf_template.html', {'model': cv})
        self.assertEquals(result == None, False)

    def test_email(self):
        msisdn = '0123456789'
        
         # setup user's firstName and surname
        post_data = {'firstName': 'Test', 'surname': 'User',  
        '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
                                        
        resp = self.client.get(reverse('send'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('send'), 'email'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'email': 'madandat@gmail.com'}
        resp = self.client.post('%s/%s' % (reverse('send'), 
                                        'email'), post_data)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')

    def test_fax(self):
        msisdn = '0123456789'
        
         # setup user's firstName and surname
        post_data = {'firstName': 'Test', 'surname': 'User', 
                     '_action': 'POST'}
        resp = self.client.get(reverse('edit_personal'), post_data, 
                               HTTP_X_UP_CALLING_LINE_ID=msisdn)
                                        
        resp = self.client.get(reverse('send'))
        self.assertEquals(resp.status_code, 200)
        
        resp = self.client.get('%s/%s' % (reverse('send'), 'fax'))
        self.assertEquals(resp.status_code, 200)
        
        post_data = {'fax': '+27123456789'}
        resp = self.client.post('%s/%s' % (reverse('send'), 
                                        'fax'), post_data)
        
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 1)
        self.assertEqual(mail.outbox[0].to[0], '+27123456789@faxfx.net')
        self.assertEqual(mail.outbox[0].from_email, 'no-reply@ummeli.org')
        self.assertEqual(len(mail.outbox[0].attachments), 1)
        self.assertEquals(mail.outbox[0].subject, 'CV for Test User')
        
