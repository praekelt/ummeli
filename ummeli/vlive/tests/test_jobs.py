from django.test import TestCase
from ummeli.vlive.jobs_util import CategoryParser,  JobsParser
from ummeli.vlive.models import Province,  Article,  Category
from ummeli.vlive import jobs_util

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
