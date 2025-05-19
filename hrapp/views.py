from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, StreamingHttpResponse
import json
import re
import time
from .langchain_sql_agent import ask_agent

def index(request):
    return render(request, 'hrapp/index.html')

@csrf_exempt
def chat_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message:
                return JsonResponse({'error': 'Empty message'}, status=400)

            def format_markdown(text):
                """Convert Markdown-like syntax to HTML using re."""
                # Bold: **text** or __text__
                text = re.sub(r'\*\*(.*?)\*\*|__(.*?)__', r'<strong>\1\2</strong>', text)
                # Italics: *text* or _text_
                text = re.sub(r'\*(.*?)\*|_(.*?)_', r'<em>\1\2</em>', text)
                # Code block: ```code``` (multiline)
                text = re.sub(r'```(.*?)```', r'<pre><code>\1</code></pre>', text, flags=re.DOTALL)
                # Inline code: `code`
                text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
                # Unordered list: - item
                lines = text.split('\n')
                in_list = False
                formatted_lines = []
                for line in lines:
                    if line.strip().startswith('- '):
                        if not in_list:
                            formatted_lines.append('<ul>')
                            in_list = True
                        formatted_lines.append(f'<li>{line[2:].strip()}</li>')
                    else:
                        if in_list:
                            formatted_lines.append('</ul>')
                            in_list = False
                        formatted_lines.append(line)
                if in_list:
                    formatted_lines.append('</ul>')
                text = '\n'.join(formatted_lines)
                # Line breaks
                text = text.replace('\n', '<br>')
                # Preprocess SQL results (wrap in code block if detected)
                if re.search(r'\b(SELECT|INSERT|UPDATE|DELETE)\b', text, re.IGNORECASE):
                    text = f'<pre><code>{text}</code></pre>'
                return text

            def stream_response():
                try:
                    # Get the full response from ask_agent
                    response = ask_agent(user_message)
                    # Format the response as HTML
                    formatted_response = format_markdown(response)
                    # Split response into chunks for streaming effect
                    words = formatted_response.split()
                    chunk_size = 3  # Number of words per chunk
                    for i in range(0, len(words), chunk_size):
                        chunk = ' '.join(words[i:i + chunk_size])
                        # Yield JSON chunk with HTML
                        yield json.dumps({'chunk': chunk}) + '\n'
                        time.sleep(0.1)  # Simulate streaming delay
                    # Final chunk to indicate completion
                    yield json.dumps({'chunk': '', 'done': True}) + '\n'
                except Exception as e:
                    yield json.dumps({'error': str(e)}) + '\n'

            return StreamingHttpResponse(
                stream_response(),
                content_type='application/json'
            )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)