from re import T
from typing import Any
import streamlit as st
import base64
import ast

# import camelot
# from camelot.core import Table
import pandas as pd 
import openai
from io import StringIO
import ast

import streamlit as st


api_key = st.sidebar.text_input("APIkey", type="password")

# st.sidebar.title( "Contributors" )
# st.sidebar.write( "- Ajaz Rana (Lead)" )
# st.sidebar.write( "- Colleague 1" )
# st.sidebar.write( "- Colleague 2" )
# st.sidebar.write( "- Colleague 3" )
# st.sidebar.write( "- Colleague 4" ) 

# st.sidebar.title( "Advisors" )
# st.sidebar.write( "- Advisor 1" )
# st.sidebar.write( "- Advisor 2" )


st.title( "NLP Laboratory" )
st.subheader( "What is your target domain?" )

# Drop downb selection for Content Source / Domain
app = st.selectbox( 'Domain s', ('Domain 1, Domain 2', 'Domain 3' , 'Domain 4', 'Domain 5' ) )

uploaded_pdf = None
file_text = None
letter_summary = None

prompt_string = None

def upload_pdf( ):

    uploaded_pdf = st.file_uploader("Choose SBC - PDF data will be Extracted and written to a TXT file", type = "pdf", key = "display_pdf")
    
    print( " line 1" ) 
    print( type( uploaded_pdf ) )
    # print( type( uploaded_pdf.name ) )
    print( "line 2" )

    if( uploaded_pdf ):
        f = uploaded_pdf.name
        print( "file name = {}".format( f ) )
    
    if uploaded_pdf is not None:
        # print ( uploaded_pdf.name )

        with open( uploaded_pdf.name, "rb" ) as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')
            # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">' 
            
            pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
            
            st.markdown( pdf_display, unsafe_allow_html = True )
            # print( type( base64_pdf ))
            # print( base64_pdf )
    return uploaded_pdf


def upload_extracted_file( ):
    uploaded_file = st.file_uploader("Uploaded PDF extract - TXT file", key = "extract_pdf" )
    print( type( uploaded_file ) )
    if uploaded_file is not None:
        print ( uploaded_file.name )
        # data = open( 'benefit_1.txt','r', encoding='utf8', errors='ignore' ).readlines()
        with open( uploaded_file.name, 'r', encoding='utf8', errors='ignore' ) as f:
            file_text = f.read()
            # st.write( file_text )
                
    return file_text


uploaded_pdf = upload_pdf()
if uploaded_pdf:
#    file_text = upload_extracted_file( )
#    st.write( file_text )

    file_name = uploaded_pdf.name

    if( file_name == "Rehab-All-Approved.pdf" ):
        prompt_string = "Read the following letter. The letter is informing the customer about the insurance company's decision for a pre-authorization request. After reading the tetter answer the question given at the end. \n\n\"\"\"\nLetter\n\nMember Name: Ajaz R Rana\nProvider Name: IVYREHAB NETWORK INC\nSetting: Office or Outpatient Facility\n\nReference Number: 14340269 \nDates of service: 10/14/2021 -12/03/2021 \n\nApproved Services: \nOffice Visits: 5 \n\nDear Ajaz Rana \n\nYour health plan requires some services to be reviewed and approved for coverage before you receive \nthem. On 11/03/2021 IVYREHAB NETWORK INC asked us to review and approve the following \nservice(s): \n\nRehabilitation Services \n\nReviewer: ASH Specialty Health Group, Inc. (ASH Group) \n\nCigna partners with ASH Group, a leading health and wellness company, to manage our Rehabilitation \nServices program. ASH Group reviews Rehabilitation Services services to determine if they are \nmedically necessary and covered by your Plan. \n\nAfter reviewing your medical information and health plan, we approved this request. \n\nImportant reminders: \n\n• When Cigna receives your medical claim(s), they'll need to malke sure your health care \nprofessionals perfomed only services we approved. If extra services were perfctrmed that weren't \nmedically necessary or covered by your plan, Cigna won't be able to pay for them. This means you'1l \nhave to pay the total cost for any extra services. \n\n• This letter isn't a guarantee that your plan will pay for the services. You must be ermolled in the plan \nand eligible for benefits on the date you receive the service. Please see your plan documents for details \nabout your coverage. You're responsible for your share of any copayments, coinsurance, or other \ncosts. \n\n• This approval is for the requested service only. It does not guarantee that the provider who requested \nthis service is in-network or will be paid at the in-network rate. This approval also does not guarantee \nthat your plan will cover services from out-of-network providers. Before you receive these services, \nplease call us to confirm whether the requesting provider is in-network. \nIf you have questions, please call Customer Service at the toll-flee number on your ID card. An associate is \navailable to help you 24 hours a day, 7 days a week. \n\nWe look forward to continuing to support you with your health and well-being. \n\nCustomer Services \n\nlf you have a hearing or speech impairment and use Telecommunications Relay Services (TRS) or a Text \nTelephone (TTY), dial 71 1 to connect with a TRS operator. \n\nSincerely,\n\ntrfupe\n\nJustine Greene, MD\nMedical Director\n\n\"\"\"\n\nQuestion: Fill in the blanks. Dear [blank= letter recipient], on [blank=date], on your behalf [blank=requestor] requested approval for [blank=requested services or procedures]. we hereby inform you that we approved [blank=what was approved and/or what was declined]. Please review the letter available on MyCigna.com for any qualifications and restrictions that may apply to this approval.\n\nAnswer:"
    elif( file_name == "Rehab-Partially-Approved.pdf"):     
        prompt_string = "Following is a letter from an insurance company to its customer informing him/her of its decision for an approval request that they had received from a provider on the customer's behalf. Read the letter and answer the question given at the end.\n\n\"\"\"\nLetter\n\n10/ 14/2021 \n\nAjaz R. Rana\n12345 CARTERET ROAD \nPRINCETON, NJ 08540 \n\nMember Name: Ajaz Rana\nProvider Name: IVYREHAB NETWORK INC\nSetting: Office or Outpatient Facility\n\nReference Number: 14340269 \n\nDear Ajaz Rana\n\nWe received your request to cover the following service(s): \n\nRehabilitation Services \n\nBased on the information we have, wc can only approve part of this request. This letter explains why. It \ndescribes your right to ask for another review. It also describes the steps you or your health care \nprofessional can take to make that request. \n\nSummary of the Coverage Decision \n\nDate Received: 10/12/2021 \n\nReviewer: American Specialty Health Group, Inc. (ASH Group) \n\nCigna Health and Life Insurance Company partners with ASH Group, a leading health and wellness \ncompany, to manage our Rehabilitation Services program. ASH Group also reviews Rehabilitation \nServices services to detemine if they are medically necessary and covered by your plan. \n\nWhat's Approved \nAfter reviewing the information we received, as well as your health plan, we determined we will cover: \n\nOfrice visits:5 \n\nImportant: In order to be covered, you must be eurolled in the plan and eligible for benefits on the date \nyou receive the service. \n\nWhats not Approved \nAt this time, we are not able to approve your request to cover: \n\nOffice Visits: 7 \n\nPlease understand: If you have or had this service, your plan will not pay for it. \n\nNote: After you receive the services we approved, your health care professional can ask us to approve \nadditional scrvices. \n\nWhy:\n \nWe reviewed information froin Ivyrehab Network Inc, your health plan and any policies and guidelines \nneeded to reach this decision. We found the service requested is not medically necessary in your case. \n\n1-OFFICE VISITS: We approve 5 visits from 10/14/2021 to 11/03/2021. These visits are for your \npost surgical spinal condition and low back pain into the upper leg. \n\nYour provider is asking for: 12 visits; From 10/14/2021; To 11/13/2021. We reviewed your records \nthat were sent to us. Based on those records, we approve: 5 of the 12 visits; From 10/14/2021; To \n11/03/2021. The other 7 visits are denied because: \n\n--Only a short course of care is approved. The findings used to support your treatment will be \noutdated at the end of the approved time period. Your provider will need to re-assess your \ncondition(s) and submit a new report. This new report should include your: complaint(s); \nsymptoms; assessment findings; updated diagnosis; response to care; and Tiew treatment. \n\n-- You have a new flare-up or exacerbation. This means that your complaints suddenly got worse. \nWe need to know your response to care before more treatment can be considered. \n\n-- Your level of function is moderately limited. We need to know your response to care before more \ntreatment can be considered. Function is your ability to do certain tasks or activities. This may \ninclude, but not limited to, tasks such as: 1) reaching; 2) bending; 3) walking; 4) pulling; 5) \ncarrying; 6) lifting. \n\nThese visits should be enough to: complete your care; or allow your provider to re-assess you and \nsubmit a new treatment plan. If you feel you need moi.e care, please talk with your provider about \nyour options.Reference: Cigna Medical Coverage Policy-Therapy Services; Physical Therapy.\nAvailable at: https://www.ashlink.com/ASH/publicffroviders/CQM/Medicalcoveragepolicies.aspx \n(3103C) Qef. Code 6) \n\nRef. Code 6 - Per the terms and conditions of your coverage, Treatment/Services that are not \ndocumented as Medically Necessary are not covered. TIIis may include, but is not limited to clinical \nlaborator}r services, I-rays, supports and appliances, and other treatments or products. \n\nIf you have questions about the information in this letter, please call Customer Service at the toll-free \nnumber on your Cigna ID card. An associate is available to help you 24 hours a day, 7 days a week. \n\nSincerely, \n\ntrfupe\n\nJustine Greene, MD \nMedical Director \n\n\"\"\"\n\nQuestion: Fill in the blanks. Dear [blank= letter recipient], on [blank=date], on your behalf [blank=requestor] requested approval for [blank=requested services or procedures]. we hereby inform you that we approved [blank=what was approved and/or what was declined]. Please review the letter available on MyCigna.com for any qualifications and restrictions that may apply to this approval.\n\nAnswer:"
    elif( file_name == "Pallavi-Inpatient.pdf" ):
        prompt_string = "Following is a letter from an insurance company to its customer informing him/her of its decision for an approval request that they had received from a provider on the customer's behalf. Read the letter and answer the question given at the end.\n\n\"\"\"\nLetter\n\nJuly 13, 2021\n\nAJAZ R RANA\n36 CARTER ROAD\nPRINCETON NJ 08540\n\nMember Name: AJAZ RANA\nProvider Name: DR. Pallavi Velagapudi, MD\nSetting: Hospital - Inpatient\n\nReviewer: Cigna Health Management, Inc. on behalf of Your Employer Plan\n\nDear Ajaz R Raun:\n\nWe want you to know that your health plan requires some care to be reviewed and approved\nbefore it is covered. On 07/12/2021, Pallavi Velagapudi, MD asked us to review and approve\ncoverage for the following service(s):\n\nInitial Inpatient\n\nAfter reviewing your medical information and health plan, we approved this request.\n\nImportant reminders:\n\nWhen we receive your medical clalm(s), we'll need to make sure your health care\nprofessionals performed only servlces we approved. If extra services were performed that\nweren't medically necessary or covered by your plan,your health plan won't be able to pay for\nthem.\n\nThis letter isn't a guarantee that your plan will pay for the services. You must be enrolled in\nthe plan and eligible for benefits on the date you receive the service. Please see your plan\ndocuments for details about your coverage. You're responsible for your share of any\ncopayments, coinsurance, or other costs.\n\nThis approval is for the requested service only. It does not guarantee that the provider who requested \nthis service is in-network or will be paid at the in-network rate. This approval also does not guarantee \nthat your plan will cover services from out-of-network providers. Before you receive these services, \nplease call us to confirm whether the requesting provider is in-network.\n\nWhile you're in the hospital, we'll work with your doctors and other health care professionals\nto get approvals for any medically necessary services covered by your plan. After you leave\nthe hospital, you and your doctor are responsible for getting approvals for additional medical\nservices.\n\nIf you have any questions. please call Customer Service at the toll-free number on your ID card.\nAn associate is available to help you 24 hours a day, 7 days a week.\n\nWe look forward to continuing to support you with your health and well-being.\n\nSincerely,\n\nGail R\n\nCigna Care Management\nGXRAHM\n\nlf you have a hearing or speech impairment and use Telecommunications Relay Services (TRS) or a\nText Telephone (lTY), dial 711 to connect with a TRS operator.\n\nC:\nPALLAVI VELAGAPUDl, MD\nPRINCETON HEAITHCARE SYSTEM\n\n\"\"\"\n\nQuestion: Fill in the blanks. Dear [blank= letter recipient], on [blank=date], on your behalf [blank=requestor] requested approval for [blank=requested services or procedures]. we hereby inform you that we approved [blank=what was approved and/or declined]. Please review the letter available on MyCigna.com for any qualifications and restrictions that may apply to this approval.\n\nAnswer:"
    elif( file_name == "Epidural-Injection.pdf"):
        prompt_string = "Following is a letter from an insurance company to its customer informing him/her of its decision for an approval request that they had received from a provider on the customer's behalf. Read the letter and answer the question given at the end.\n\n\"\"\"\nLetter\n\nJune 25, 2021\n\nAjaz R Rana\n36 Carter Road\nPrinceton, NJ 08540\n\nMember Name: AJAZ RANA\nProvider Name: Dr. Jeffery Miller, MD\nSetting: Office or Outpatient Facility\n\nDear Ajaz Rana:\n\nWe want you to know your health plan requires some care to be reviewed and approved before it's\ncovered. On June 25, 2021, Dr. Jeffery Miller asked us to review and approve coverage for the\nfollowing service(s):\n\n1 unit of 64483: Injection(s), anesthetic agent(s), and/or steroid; transforaminal epidural, with\nimaging guidance (fluoroscopy or CT), lumbar or sacral, single level Modifier: LT\n\nReviewer: eviCore Healthcare (eviCore)\n\nCigna partners with eviCore, a leading health and wellness company, to manage our musculoskeletal\nprogram. eviCore reviews musculoskeletal services to detremine if they are medically necessary and\ncovered by your plan.\n\nAfter reviewing your medical information and health plan, we approved this request.\n\nImportant Reminders:\n\nWhen we receive your medical clalm(s), we'll need to make sure your health care\nprofessionals performed only servlces we approved. If extra services were performed that\nweren't medically necessary or covered by your plan,your health plan won't be able to pay for\nthem. This means you'll have to pay the total cost for any extra services.\n\nThis letter isn't a guarantee that your plan will pay for the services. You must be enrolled in\nthe plan and eligible for benefits on the date you receive the service. Please see your plan\ndocuments for details about your coverage. You're responsible for your share of any\ncopayments, coinsurance, or other costs.\n\nlf you have questions, please call Customer Service at the toll-free number on your lD card. An\nassociate is available to help you 24 hours a day, 7 days a week.\n\nWe look forward to continuing to support you with your health and well-being.\n\nSincerely,\n\nevicore healthcare\nMusculoskeletal Utilization Management Programs\n\nlf you have a hearing or speech impairment and use Telecommunications Relay Services (TRS) or a\nText Telephone (lTY), dial 711 to connect with a TRS operator.\n\nCC: Dr. Jeffery Miller, Fax: 609/613-5929\nPrinceton Princeton orthopaedic Associates, Fax: 609/924-8532\n\n\"\"\"\n\nQuestion: Fill in the blanks. Dear [blank= letter recipient], on [blank=date], on your behalf [blank=requestor] requested approval for [blank=requested services or procedures]. we hereby inform you that we approved [blank=what was approved and/or declined]. Please review the letter available on MyCigna.com for any qualifications and restrictions that may apply to this approval.\n\nAnswer:"
    elif( file_name == "Surgery.pdf"):
        prompt_string = "Following is a letter from an insurance company to its customer informing him/her of its decision for an approval request that they had received from a provider on the customer's behalf. Read the letter and answer the question given at the end.\n\n\"\"\"\nLetter\n\nAugust 5, 2021\n\nAjaz R Rana\n36 Carter Road\nPrinceton, NJ 08540\n\nMember Name: AJAZ RANA\nProvider Name: Dr. David Lamb\nSetting: Hospital - Outpatient\n\nReviewer: Cigna Health Management, Inc. on behalf of Your Employer Plan\n\nDear Ajaz R Rana:\n\nWe want you to know that your health plan requires some care to be reviewed and approved\nbefore it is covered. On 08/05/2021, David J Lamb, MD asked us to review and approve coverage\nfor the following service(s):\n\n• 63047 Partial removal of middle spine bone with release of spinal cord and/or nerves\n• 63030 Partial removal of bone with release of spinal cord or spinal nerves of I interspace in lower spine\n• 63048 Partial removal of spine bone with release of spinal cord and/or nerves\n\nAfter reviewing your medical information and health plan, we approved this request.\n\nImportant reminders:\n\nWhen we receive your medical clalm(s), we'll need to make sure your health care\nprofessionals performed only servlces we approved. If extra services were performed that\nweren't medically necessary or covered by your plan,your health plan won't be able to pay for\nthem.\n\nThis letter isn't a guarantee that your plan will pay for the services. You must be enrolled in\nthe plan and eligible for benefits on the date you receive the service. Please see your plan\ndocuments for details about your coverage. You're responsible for your share of any\ncopayments, coinsurance, or other costs.\n\nThis approval is for the requested service only. It does not guarantee that the provider who requested \nthis service is in-network or will be paid at the in-network rate. This approval also does not guarantee \nthat your plan will cover services from out-of-network providers. Before you receive these services, \nplease call us to confirm whether the requesting provider is in-network.\n\nWhile you're in the hospital, we'll work with your doctors and other health care professionals\nto get approvals for any medically necessary services covered by your plan. After you leave\nthe hospital, you and your doctor are responsible for getting approvals for additional medical\nservices.\n\nIf you have any questions. please call Customer Service at the toll-free number on your ID card.\nAn associate is available to help you 24 hours a day, 7 days a week.\n\nWe look forward to continuing to support you with your health and well-being.\n\nSincerely,\n\nCigna Utilization Management Services\n\nlf you have a hearing or speech impairment and use Telecommunications Relay Services (TRS) or a\nText Telephone (lTY), dial 711 to connect with a TRS operator.\n\nC:\nDAVID J LAMB, MD\nPRINCETON HEALTHCARE SYSTEM\n\n\"\"\"\n\nQuestion: Fill in the blanks. Dear [blank= letter recipient], on [blank=date], on your behalf [blank=requestor] requested approval for [blank=requested services or procedures]. we hereby inform you that we approved [blank=what was approved and/or declined]. Please review the letter available on MyCigna.com for any qualifications and restrictions that may apply to this approval.\n\nAnswer:"

    print( file_name )
    # print( prompt_string )

    expander = st.expander("See Text")
    expander.write( prompt_string )

    #st.write( file_name )
    # st.write( prompt_string )

    pressed = st.button( "submit", key = "run prediction" )

    if( pressed ):
        print( "Button Pressed and Application = {}".format( app ) )
        print( "Lets get letter Summary" )

        openai.api_key=api_key

        response = openai.Completion.create(
        model="davinci-instruct-beta",
        prompt = prompt_string,
        
        # this should stay commented
        # prompt="Read the following letter. The letter is informing the customer about the insurance company's decision for a pre-authorization request. After reading the tetter answer the question given at the end. \n\n\"\"\"\nLetter\n\nMember Name: Ajaz Rana\nProvider Name: IVYREHAB NETWORK INC\nSetting: Office or Outpatient Facility\n\nReference Number: 14340269 \nDates of service: 10/14/2021 -12/03/2021 \n\nApproved Services: \nOffice Visits: 5 \n\nDear Ajaz Rana \n\nYour health plan requires some services to be reviewed and approved for coverage before you receive \nthem. On 11/03/2021 IVYREHAB NETWORK INC asked us to review and approve the following \nservice(s): \n\nRehabilitation Services \n\nReviewer: ASH Specialty Health Group, Inc. (ASH Group) \n\nCigna partners with ASH Group, a leading health and wellness company, to manage our Rehabilitation \nServices program. ASH Group reviews Rehabilitation Services services to determine if they are \nmedically necessary and covered by your Plan. \n\nAfter reviewing your medical information and health plan, we approved this request. \n\nImportant reminders: \n\n• When Cigna receives your medical claim(s), they'll need to malke sure your health care \nprofessionals perfomed only services we approved. If extra services were perfctrmed that weren't \nmedically necessary or covered by your plan, Cigna won't be able to pay for them. This means you'1l \nhave to pay the total cost for any extra services. \n\n• This letter isn't a guarantee that your plan will pay for the services. You must be ermolled in the plan \nand eligible for benefits on the date you receive the service. Please see your plan documents for details \nabout your coverage. You're responsible for your share of any copayments, coinsurance, or other \ncosts. \n\n• This approval is for the requested service only. It does not guarantee that the provider who requested \nthis service is in-network or will be paid at the in-network rate. This approval also does not guarantee \nthat your plan will cover services from out-of-network providers. Before you receive these services, \nplease call us to confirm whether the requesting provider is in-network. \nIf you have questions, please call Customer Service at the toll-flee number on your ID card. An associate is \navailable to help you 24 hours a day, 7 days a week. \n\nWe look forward to continuing to support you with your health and well-being. \n\nCustomer Services \n\nlf you have a hearing or speech impairment and use Telecommunications Relay Services (TRS) or a Text \nTelephone (TTY), dial 71 1 to connect with a TRS operator. \n\nSincerely,\n\ntrfupe\n\nJustine Greene, MD\nMedical Director\n\n\"\"\"\n\nQuestion: Fill in the blanks. Dear [blank], on your behalf [blank] requested approval for [blank]. They requested [blank]. we hereby inform you that we approved [blank].\n\nAnswer:",
        
        temperature=0.7,
        # temperature=0.0,
        max_tokens=175,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
        )

        
        print( response )
        st.write( response )

        # st.json( response )

    else:
        print( "No Button Pressed" )




# to run the app
# streamlit run GPT3-PreAuth.py
# streamlit run GPT3-PreAuth.py --server.port 5998