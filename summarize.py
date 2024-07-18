import click
import requests
import json

def summarize_text(model, prompt):
    url='http://localhost:11434/api/generate'
    headers={'Content-Type':'application/json'}
    data={"model": model,"prompt": prompt}

    response=requests.post(url,headers=headers,json=data)

    if(response.status_code==200):
        response_parts=[]  #print(f"Response Content:{response.text}") 
        for line in response.iter_lines():
            if line:
                response_json=json.loads(line)
                response_parts.append(response_json.get('response', ''))
                
        summary=' '.join(response_parts)
        return summary
    else:
        click.echo(f"Request failed: {response.text}")
   
@click.command()
@click.option('--input_file', type=click.File('r',encoding='utf-8'), help="The file to read")
@click.option('--text', type=str, help="The text to read")
def read_input(input_file, text):
    if input_file:
        input_text=input_file.read()
    elif text:
        input_text=text
    else:
        click.echo("File or text not found")
        return

    model="qwen2:0.5b"
    prompt=f"Summarize the text:{input_text}"
    summary=summarize_text(model, prompt)
    if summary:
        click.echo(f"Summary:{summary}")

if __name__ == '__main__':
    read_input()
