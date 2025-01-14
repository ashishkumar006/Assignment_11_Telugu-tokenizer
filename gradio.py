import gradio as gr
from tokenizers import Tokenizer

# Load your trained Telugu tokenizer (replace with the correct path)
tokenizer = Tokenizer.from_file("telugu_tokenizer.json")

# Function to encode text and display additional info
def encode_text(input_text):
    tokens = tokenizer.encode(input_text)
    token_count = len(tokens.tokens)
    compression_ratio = len(input_text) / token_count if token_count != 0 else 0
    token_list = tokens.tokens
    
    # Highlight tokens (color coding for visualization)
    token_colors = [
        f"<span style='background-color: #{hash(token) % 0xFFFFFF:06x};'>{token}</span>"
        for token in token_list
    ]
    token_highlighted = " ".join(token_colors)
    
    return token_count, round(compression_ratio, 3), token_highlighted, token_list

# Function to decode tokens into text
def decode_tokens(input_tokens):
    try:
        # Parse input tokens as a list of strings
        token_list = eval(input_tokens) if isinstance(input_tokens, str) else input_tokens
        decoded_text = tokenizer.decode(token_list)
        return decoded_text
    except Exception as e:
        return f"Error: {e}"

# Define the Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# Telugu Text Tokenizer")
    
    # Tabs for Encode and Decode
    with gr.Tabs():
        # Encode Tab
        with gr.Tab("Encode"):
            gr.Markdown("### Encode Text")
            input_text = gr.Textbox(
                label="Input Text", 
                placeholder="Enter Telugu text to tokenize...", 
                lines=3
            )
            token_count = gr.Number(label="Token Count")
            compression_ratio = gr.Number(label="Compression Ratio")
            token_highlighted = gr.HTML(label="Token Visualization")
            token_list = gr.JSON(label="Token List")
            encode_btn = gr.Button("Encode")
            
            # Connect the encode button to the encode_text function
            encode_btn.click(
                encode_text,
                inputs=[input_text],
                outputs=[token_count, compression_ratio, token_highlighted, token_list]
            )
        
        # Decode Tab
        with gr.Tab("Decode"):
            gr.Markdown("### Decode Tokens")
            input_tokens = gr.Textbox(
                label="Input Tokens", 
                placeholder='Enter token list (e.g., ["token1", "token2"])',
                lines=3
            )
            decoded_text = gr.Textbox(
                label="Decoded Text", 
                placeholder="The decoded text will appear here..."
            )
            decode_btn = gr.Button("Decode")
            
            # Connect the decode button to the decode_tokens function
            decode_btn.click(
                decode_tokens,
                inputs=[input_tokens],
                outputs=[decoded_text]
            )

# Launch the Gradio app
demo.launch()
