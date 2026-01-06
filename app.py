import streamlit as st
from markitdown import MarkItDown
import os
import tempfile

def format_size(bytes_size):
    """Formats bytes into a human-readable string."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"

def main():
    st.set_page_config(page_title="Universal File-to-Text Converter", page_icon="📄")
    
    st.title("📄 Universal File-to-Text")
    st.markdown("Convert Office docs and PDFs into clean **Markdown** or **Text** instantly.")

    md_engine = MarkItDown()

    uploaded_files = st.file_uploader(
        "Drag and drop files here", 
        type=["docx", "xlsx", "pptx", "pdf", "html", "htm"], 
        accept_multiple_files=True
    )

    if uploaded_files:
        st.divider()
        
        for uploaded_file in uploaded_files:
            # Metadata and Sizing
            orig_size = uploaded_file.size
            file_extension = os.path.splitext(uploaded_file.name)[1].lower()
            base_name = os.path.splitext(uploaded_file.name)[0]
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp_file:
                tmp_file.write(uploaded_file.getvalue())
                tmp_path = tmp_file.name

            try:
                # [1] Conversion Engine
                result = md_engine.convert(tmp_path)
                content = result.text_content
                
                # Calculate converted size
                conv_size = len(content.encode('utf-8'))
                reduction = ((orig_size - conv_size) / orig_size) * 100 if orig_size > 0 else 0

                st.subheader(f"📄 {uploaded_file.name}")

                # [2] Interface: Tabs for Preview and Size Analysis
                tab1, tab2 = st.tabs(["🔍 Instant Preview", "📊 File Size Comparison"])

                with tab1:
                    st.text_area(
                        label="Markdown Content",
                        value=content,
                        height=300,
                        key=f"text_{uploaded_file.name}"
                    )
                    
                    # Download Buttons
                    c1, c2 = st.columns(2)
                    c1.download_button("Download .md", content, f"{base_name}_converted.md", "text/markdown", key=f"m_{uploaded_file.name}")
                    c2.download_button("Download .txt", content, f"{base_name}_converted.txt", "text/plain", key=f"t_{uploaded_file.name}")

                with tab2:
                    # [3] Comparison Table
                    st.table({
                        "Metric": ["Original File Size", "Converted Text Size"],
                        "Value": [format_size(orig_size), format_size(conv_size)]
                    })
                    
                    if reduction > 0:
                        st.success(f"📈 **Text version is {reduction:.1f}% smaller** than the original file.")
                    else:
                        st.info("The text version is roughly the same size as the original.")

            except Exception as e:
                st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")

            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            st.divider()

if __name__ == "__main__":
    main()
