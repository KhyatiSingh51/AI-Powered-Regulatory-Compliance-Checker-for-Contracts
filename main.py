import streamlit as st
import agreement_comparision
import data_extraction
import json
import schedule
import threading
import time
import scrapping
import notification

# ******** Phase 2 ******** #
# if __name__ == "__main__":
    
    
#     unseen_file = "document to compare/Controller-to-Controller-Agreement-1.pdf"
    
#     # step 1: identify the type of agreement
#     agreement_type = agreement_comparision.document_type(unseen_file)
#     print("Document Type: ", agreement_type)
    
#     if agreement_type == "Data Processing Agreement":
        
        
#         # Step 2: Extract clause data from agreement 
#         unseen_data = data_extraction.Clause_extraction(unseen_file)
        
#         # Step 2 with summarization:
#         # unseen_data = data_extration.Clause_extraction_with_summarization(unseen_file)
        
#         # Step 3: Fetch stored template data
#         with open("dpa.json", "r", encoding="utf-8") as f:
#             template_data = json.load(f)
        
#         # Step 4: Compare the unseen data with template data
#         result = agreement_comparision.compare_agreements(unseen_data, template_data)
    
#     elif agreement_type == "Controller-to-Controller Agreement":
        
        
#         with open(r"json_files/c2c.json", "r", encoding="utf-8") as f:
#             template_data = json.load(f)
#         # Step 2: Extract clause data from agreement 
#         unseen_data = data_extraction.Clause_extraction(unseen_file)
        
#         # Step 2 with summarization:
#         # unseen_data = data_extration.Clause_extraction_with_summarization(unseen_file)
        
#         # Step 3: Fetch stored template data
        
        
#         # Step 4: Compare the unseen data with template data
#         result = agreement_comparision.compare_agreements(unseen_data, template_data)
#         # Mapping of agreement type to respective JSON file


def run_scheduler():
    # call call_scrape_function every night at 12 am
    # schedule.every().day.at("00:00").do(scraping.call_scrape_function)

    # schedule.every(10).seconds.do(scrapping.call_scrape_funtion)

    schedule.every(1).minutes.do(scrapping.call_scrape_funtion)

    while True:
        schedule.run_pending()
        time.sleep(1)  # check every 5 seconds


# Start scheduler in background thread so Streamlit doesn’t block
threading.Thread(target=run_scheduler, daemon=True).start()


if __name__ == "__main__":
    try:
        AGREEMENT_JSON_MAP = {
            "Data Processing Agreement":"json_file/dpa.json",
            "Joint Controller Agreement": "json_file/jca.json",
            "Controller-to-Controller Agreement":"json_file/c2c.json",
            "Processor-to-Subprocessor Agreement":"json_file/subprocessor.json",
            "Standard Contractual Clauses": "json_file/scc.json"
        }

        # Streamlit Title
        st.title("📄 Contract Compliance Checker")

        # File upload section
        uploaded_file = st.file_uploader("Upload an agreement (PDF only)", type=["pdf"])

        if uploaded_file is not None:
            # Save uploaded file temporarily
            with open("temp_uploaded.pdf", "wb") as f:
                f.write(uploaded_file.read())

            st.info("Processing your file... Please wait ⏳")

            # Step 1: Identify document type
            agreement_type = agreement_comparision.document_type("temp_uploaded.pdf")
            st.write("**Detected Document Type:**", agreement_type)

            # Check if template exists for detected type
            if agreement_type in AGREEMENT_JSON_MAP:
                # Step 2: Extract clause data with Groq fallback
                try:
                    unseen_data = data_extraction.Clause_extraction_with_summarization("temp_uploaded.pdf")
                    st.success("✅ Clause Extraction Completed")
                except Exception as e:
                    if "overload" in str(e).lower():
                        st.warning("Model overloaded! Switching to Groq accelerated processing...")
                        unseen_data = data_extraction.Clause_extraction_with_summarization_groq("temp_uploaded.pdf")
                        st.success("✅ Clause Extraction Completed via Groq")
                    else:
                        raise e  # let outer except block handle other errors

                # Step 3: Load respective template JSON
                template_file = AGREEMENT_JSON_MAP[agreement_type]
                with open(template_file, "r", encoding="utf-8") as f:
                    template_data = json.load(f)

                # Step 4: Compare agreements
                result = agreement_comparision.compare_agreements(unseen_data, template_data)

                # Display result
                st.subheader("🧾 Comparison Result")
                st.write(result)

                # Send notification
                body = f"Agreement type is {agreement_type} \n Comparison Result: {result}"
                notification.send_notification("Comparison Result", body)

            else:
                st.error("This document is not under GDPR compliance")

    except Exception as e:
        # Outer exception handling for all other errors
        print("Error Occurred in document comparison:", e)
        notification.send_notification("Error Occurred in document comparison", str(e))
        st.error(f"We are facing some issue: {e}")