import streamlit as st
from markitdown import MarkItDown
import os
import tempfile

# Configuration for stability (User-Agent and Timeout)
# Note: MarkItDown uses standard requests internally for URLs.
HTTP_CONFIG = {
    "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"},
    "timeout": 5
}

def main():
    st.set_page_config(page_title="Universal File-to-Text Converter", page_icon="📄")
    
    st.title("📄 Universal File-to-Text")
    st.markdown("Convert Word, Excel, PPT, PDF, and HTML into clean **Markdown** or **Text** instantly.")

    # [1] Initialize the Engine
    # We pass the custom config for any internal web requests the engine might make
    md_engine = MarkItDown()

    # [2] Interface: Upload Area
    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "htm"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.divider()
        
        for uploaded_file in uploaded_files:
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            # Use a temporary file to interface with MarkItDown
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            try:
                # [1] The Engine Processing
                result = md_engine.convert(tmp_path)
                content = result.text_content

                # [2] Interface: Instant Preview
                with st.expander(f"Preview: {uploaded_file.name}", expanded=True):
                    st.text_area(
                        label="Converted Content",
                        value=content,
                        height=300,
                        key=f"text_{uploaded_file.name}"
                    )

                    # [2] Interface: Download Options
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.download_button(
                            label="Download as Markdown (.md)",
                            data=content,
                            file_name=f"{base_name}_converted.md",
                            mime="text/markdown",
                            key=f"md_{uploaded_file.name}"
                        )
                    
                    with col2:
                        st.download_button(
                            label="Download as Text (.txt)",
                            data=content,
                            file_name=f"{base_name}_converted.txt",
                            mime="text/plain",
                            key=f"txt_{uploaded_file.name}"
                        )

            except Exception as e:
                # [3] Resilience: Error Handling
                st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
                # Optional: st.info(f"Debug Info: {e}") 

            finally:
                # Cleanup temporary file
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)

if __name__ == "__main__":
    main()
