'''
https://statejobs.ny.gov/public/vacancyTable.cfm?searchResults=Yes&Keywords=&title=&JurisClassID=&AgID=&minDate=&maxDate=&cat10=10&employmentType=&grade=&SalMin=
https://statejobs.ny.gov/public/vacancyTable.cfm?searchResults=Yes&Keywords=&title=&JurisClassID=&AgID=&minDate=&maxDate=&{}&employmentType=&grade=&SalMin=
<p class="row">
				<span class="leftCol">
					In the Category
					</span><span class="rightCol">
					<input name="cat1" type="checkbox" value="1" id="cat1"><label for="cat1">Clerical, Secretarial, Office Aide</label><br>
					<input name="cat2" type="checkbox" value="2" id="cat2"><label for="cat2">Financial, Accounting, Auditing</label><br>
					<input name="cat3" type="checkbox" value="3" id="cat3"><label for="cat3">Education, Teaching</label><br>
					<input name="cat4" type="checkbox" value="4" id="cat4"><label for="cat4">Other Professional Careers</label><br>
					<input name="cat5" type="checkbox" value="5" id="cat5"><label for="cat5">Skilled Craft, Apprenticeship, Maintenance</label><br>
					<input name="cat6" type="checkbox" value="6" id="cat6"><label for="cat6">Health Care, Human/Social Services</label><br>
					<input name="cat7" type="checkbox" value="7" id="cat7"><label for="cat7">I.T. Engineering, Sciences</label><br>
					<input name="cat8" type="checkbox" value="8" id="cat8"><label for="cat8">Administrative or General Management</label><br>
					<input name="cat9" type="checkbox" value="9" id="cat9"><label for="cat9">Enforcement or Protective Services</label><br>
					<input name="cat10" type="checkbox" value="10" id="cat10"><label for="cat10">Legal</label><br>
					<input name="cat99" type="checkbox" value="99" id="cat99"><label for="cat99">No Preference</label><br>
					
				</span>
			</p>
			
			
Clerical, Secretarial, Office Aide			= cat1=1
Financial, Accounting, Auditing				= cat2=2
Education, Teaching 						= cat3=3
Other Professional Careers 					= cat4=4
Skilled Craft, Apprenticeship, Maintenance	= cat5=5
Health Care, Human/Social Services 			= cat6=6
I.T. Engineering, Sciences 					= cat7=7
Administrative or General Management 		= cat8=8
Enforcement or Protective Services 			= cat9=9
Legal										= cat10=10


'''
#sortUrl = f'https://statejobs.ny.gov/public/vacancyTable.cfm?searchResults=Yes&Keywords=&title=&JurisClassID=&AgID=&minDate=&maxDate=&{}&employmentType=&grade=&SalMin='

def sortUrlMaker(category):
	catUrlOut = f'https://statejobs.ny.gov/public/vacancyTable.cfm?searchResults=Yes&Keywords=&title=&JurisClassID=&AgID=&minDate=&maxDate=&cat{category}={category}&employmentType=&grade=&SalMin='
	return catUrlOut

def catOptionsFunc():
	print("Here are your options: ")
	print("Clerical, Secretarial, Office Aide			=	 1")
	print("Financial, Accounting, Auditing				=	 2")
	print("Education, Teaching 							=	 3")
	print("Other Professional Careers 					=	 4")
	print("Skilled Craft, Apprenticeship, Maintenance	=	 5")
	print("Health Care, Human/Social Services 			=	 6")
	print("I.T. Engineering, Sciences 					=	 7")
	print("Administrative or General Management 		=	 8")
	print("Enforcement or Protective Services 			=	 9")
	print("Legal										=	 10")
	


# Do they want to sort?
wantSort = print("Do you want to sort by type? (Y or N)\n")
# Make sure it is valid
while ((wantSort != 'Y') and (wantSort != 'N')):
	wantSort = print("I'm sorry, answer either Y for yes or N for no...\n")
	
if (wantSort == 'Y'):

	# If they want it sorted, give them the options and let them pic
	catOptionsFunc()

	# have them choose
	chooseCategory = print("\nWhich do you want?\n")
	categoryNums = [1,2,3,4,5,6,7,8,9,10]
	#while(chooseCategory != 1 || != 2 || != 3 || != 4 || != 5 || != 6 || != 7 || != 8 || != 9 || != 10 )
	while chooseCategory not in categoryNums:
		catOptionsFunc()
		chooseCategory = print("\nThat was invalid, choose one of the above: ")
		
	# create url and then submit
	searchCatUrl = sortUrlMaker(chooseCategory)
	
	print(searchCatUrl)
	
	# Get Even Designated Jobs CSV
	
	

	
	
# -=-=-=-=-=-=-=-=-
	outputNameCat = ''
	if (chooseCategory == 1):
		outputNameCat = ' Clerical_Secretarial_Office Aide '
	if (chooseCategory == 2):
		outputNameCat = ' Financial_Accounting_Auditing '
	if (chooseCategory == 3):
		outputNameCat = ' Education_Teaching '
	if (chooseCategory == 4):
		outputNameCat = ' Other Professional Careers '
	if (chooseCategory == 5):
		outputNameCat = ' Skilled Craft_Apprenticeship_Maintenance '
	if (chooseCategory == 6):
		outputNameCat = ' Health Care_Human Services_Social Services '
	if (chooseCategory == 7):
		outputNameCat = ' IT_Engineering_Sciences '
	if (chooseCategory == 8):
		outputNameCat = ' Administrative_General Management '
	if (chooseCategory == 9):
		outputNameCat = ' Enforcement_Protective Services '
	if (chooseCategory == 10):
		outputNameCat = ' Legal '
		
		
	getJobs(url,f"{outputNameCat}{use_this_datetime}")
	
	

