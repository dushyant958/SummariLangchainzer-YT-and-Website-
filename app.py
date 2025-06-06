import validators, streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

# Setting up page configuration
st.set_page_config(
    page_title = " SummariLangchainzer (YT and Website)",
    page_icon = "🦅 ",
    layout="wide",
    initial_sidebar_state= "expanded",
)
st.title("SummariLangchainzer (YT and Website)")
st.subheader("Summarizes given URL")

# Get the GROQ API KEY and URL to be suummarized
with st.sidebar:
    groq_api_key = st.text_input("Enter your GROQ API Key", type = "password")

# URL Processing
st.subheader("Enter URL/URLs to be summarized")
url_input_method = st.radio(
    "Choose input method for URL",
    ["Single URL", "Multiple URLs (one per line)", "Upload text file with URLs"]
) 

urls_to_process = []

if url_input_method == "Single URL":
    single_url = st.text_input("URL", 
                               placeholder="Enter a single URL to summarize")
    if single_url.strip():
        urls_to_process.append(single_url.strip())

elif url_input_method == "Multiple URLs (one per line)":
    multiple_urls = st.text_area("" \
    "Enter URLs (one per line)",
    placeholder="https://youtube.com/watch?v=example1\nhttps://example.com/article1\nhttps://example.com/article2",
    height = 150)
    if multiple_urls.strip():
        urls_to_process = [url.strip() for url in multiple_urls.split("\n") if url.strip()]

elif url_input_method == "Upload text file with URLs":
    uploaded_file = st.file_uploader("Choose a text file", type=['txt'])
    if uploaded_file is not None:
        content = uploaded_file.read().decode('utf-8')
        urls_to_process = [url.strip() for url in content.split('\n') if url.strip()]

# Displaying URLs to be processed
if urls_to_process:
    st.write(f"📊 **{len(urls_to_process)} URL(s) ready for processing:**")
    for i, url in enumerate(urls_to_process, 1):
        st.write(f"{i}. {url}")

st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    summary_length = st.selectbox(
        "📏 Summary Length:",
        ["Brief", "Medium", "Detailed"],
        index=1  # Default to Medium
    )

with col2:
    summary_style = st.selectbox(
        "✍️ Summary Style:",
        ["Paragraph", "Bullet Points", "Key Highlights"],
        index=0
    )

# Prompt template section
def get_custom_prompt(length, style):
    """Generate custom prompt based on user preferences"""
    
    length_instructions = {
        "Brief": "Provide a concise summary in 2-3 sentences focusing only on the main points.",
        "Medium": "Provide a balanced summary in 1-2 paragraphs covering key points and important details.",
        "Detailed": "Provide a comprehensive summary with detailed explanations, context, and supporting information."
    }
    
    style_instructions = {
        "Paragraph": "Write the summary in well-structured paragraphs.",
        "Bullet Points": "Format the summary as clear bullet points with main ideas.",
        "Key Highlights": "Present the summary as numbered key highlights with brief explanations."
    }
    
    prompt_template = f"""
    You are a helpful assistant that summarizes content from URLs.
    
    Length Requirement: {length_instructions[length]}
    Format Requirement: {style_instructions[style]}
    
    Content to summarize: {{text}}
    
    Please provide a {length.lower()} summary following the {style.lower()} format.
    Make sure the summary is informative, accurate, and well-organized.
    """
    
    return PromptTemplate(
        template=prompt_template,
        input_variables=["text"]
    )

if st.button("🚀 Summarize Content"):
    # Validation
    if not groq_api_key.strip():
        st.error("⚠️ Please provide your GROQ API Key")
    elif not urls_to_process:
        st.error("⚠️ Please provide at least one valid URL")
    else:
        # Validating all URLs
        invalid_urls = [url for url in urls_to_process if not validators.url(url)]
        if invalid_urls:
            st.error(f"❌ Invalid URLs found: {', '.join(invalid_urls)}")
        else:
            try:
                # Llama Model being used
                llm = ChatGroq(model = "Llama3-8b-8192",
                               groq_api_key = groq_api_key)
                
                # Custom prompt based on user preferences
                prompt = get_custom_prompt(summary_length, summary_style)
                
                # Progress bar for multiple URLs
                progress_bar = st.progress(0)
                results = []
                
                for i, url in enumerate(urls_to_process):
                    st.write(f"🔄 Processing URL {i+1}/{len(urls_to_process)}: {url}")
                    
                    with st.spinner(f"Loading content from URL {i+1}..."):
                        # Data Loading process
                        if "youtube.com" in url or "youtu.be" in url:
                            loader = YoutubeLoader.from_youtube_url(url, add_video_info=True)
                        else:
                            loader = UnstructuredURLLoader(
                                urls=[url], 
                                ssl_verify=False,
                                headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
                            )
                        
                        data = loader.load()
                        
                        # Summarization chain
                        chain = load_summarize_chain(llm, chain_type='stuff', prompt=prompt, verbose=False)
                        summary = chain.run(data)
                        
                        # Store summary
                        final_summary = str(summary).strip()
                        
                        results.append({
                            'url': url,
                            'summary': final_summary,
                        })
                        
                        # Progress bar
                        progress_bar.progress((i + 1) / len(urls_to_process))
                
                # Displaying the results
                st.success(f"✅ Successfully processed {len(results)} URL(s)!")
                
                for i, result in enumerate(results, 1):
                    with st.expander(f"📄 Summary {i}: {result['url'][:50]}..."):
                        # Display the summary
                        st.write("**Summary:**")
                        st.write(result['summary'])
                        
                        st.markdown("---")
                        
                        # Download button for summary
                        st.download_button(
                            label=f"📥 Download Summary {i}",
                            data=result['summary'],
                            file_name=f"summary_{i}.txt",
                            mime="text/plain"
                        )
                        
            except Exception as e:
                st.error(f"❌ An error occurred: {str(e)}")
                st.exception(e)
