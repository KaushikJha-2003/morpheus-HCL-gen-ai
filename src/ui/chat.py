"""
Chat interface UI components.
"""
import streamlit as st
from src.rag.chain import create_rag_chain


def render_chat_interface():
    """Render the main chat interface."""
    st.title("Intellicite: AI Document Assistant")
    st.markdown("---")
    
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    
    # Chat input
    user_input = st.chat_input("Ask something about your document...")
    
    if user_input:
        if not st.session_state.vectorstore:
            st.warning("Process a document first.")
        else:
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Display user message
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Generate and display assistant response
            with st.spinner("Thinking..."):
                try:
                    chain = create_rag_chain(
                        st.session_state.vectorstore,
                        st.session_state.llm,
                        st.session_state.persona_select
                    )
                    
                    if chain:
                        answer = chain.invoke(user_input)
                        st.session_state.messages.append({"role": "assistant", "content": answer})
                        
                        with st.chat_message("assistant"):
                            st.markdown(answer)
                    else:
                        error_msg = "Failed to create RAG chain. Please try again."
                        st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.error(error_msg)
                
                except Exception as e:
                    error_msg = f"Error generating answer: {e}"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    st.error(error_msg)
    
    st.markdown("---")

