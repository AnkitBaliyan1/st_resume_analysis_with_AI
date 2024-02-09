import streamlit as st
import uuid
from utils import *
from dotenv import load_dotenv

if "unique_id" not in st.session_state:
    st.session_state["unique_id"]=''


def main():
    load_dotenv()

    st.set_page_config(page_title = "Resume Screening Assistance")
    st.title("HR - Resume Screening Assistance..")
    st.subheader("I can help you with resume screening process")

    job_description = st.text_area("Please paste the Job Description here...", key="1")
    document_count = st.text_input("Number of \"RESUME\" to return", key="2")
    # upload the resume (pdf)
    pdf = st.file_uploader("Upload resume here, Only PDF file allowed", type=["pdf"], accept_multiple_files=True)

    submit = st.button("Help me with Analysis")

    if submit:
        with st.spinner("Analysis in progress .. "):
            #st.write("Analysis in progress")

            # creating unique ID, to store vector in pinecone and reterive as and when required
            st.session_state["unique_id"] = uuid.uuid4().hex

            # create document list our of all the pdf uploaded by user
            docs = create_docs(pdf, st.session_state["unique_id"])
            #st.write(docs)

            # displaying to count of document updloaded
            st.write("Analyzing",len(docs), "Resume.")

            # creating embedding instance
            embeddings = create_embedding_instance()
            #st.write("Embedding instance created")

            # pushing data to Pinecone
            #with st.spinner("Uploading doc to pinecone"):
            push_to_pinecone(embeddings,docs)

            # Fetch relavent docs from Pinecone
            relavent_doc = get_similar_doc(job_description, document_count, embeddings,st.session_state["unique_id"])
            #st.write("Relavent docs are below")
            #st.write(relavent_doc)

            # displaying some info of relavent doc
            for item in range(len(relavent_doc)):
                st.subheader("👉🏻 "+str(item+1))
                
                # file path
                st.write("**File** : "+relavent_doc[item][0].metadata['name'] )

                with st.expander("Show me 👀"):
                    st.info("**Match Score** : "+ str(relavent_doc[item][1]))

                    summary = get_summary(relavent_doc[item][0])
                    st.write("**Summary** : " + summary)

        st.success("Hope I was able to save your time")



if __name__=="__main__":
    main()
