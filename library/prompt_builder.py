#Skapar prompten som används vid API anropet till OpenAI
#🧠 GPT prioriterar:
#Tydliga instruktioner i prompten
#Tidigare innehåll i prompten (det som kommer först)
#Det som är mest konkret och strukturerat
#➡️ Det betyder att intervjuanteckningar vinner över transcriptet i nästan alla fall – så länge prompten säger det.


def create_prompt(doc_text, mall_text, style_text, transcript_text=None):
        if transcript_text:
            transcript_section = f"""
📚 This is a complementary transcript from the interview.  
🟡 Use it *only* to support or expand upon the information in the interview notes.  
🟡 If there are discrepancies – prioritize the interview notes.  
🟡 You do not need to summarize the entire transcript – only extract relevant details:
{transcript_text}
"""
        else:
            transcript_section = ""
        return f"""
You are a professional recruiter tasked with writing a detailed summary based on an interview.

📄 Below are the interview notes about the candidate:
{doc_text}
{transcript_section}

🎯 Your task:
1. Write a highly detailed and structured summary based on the interview notes (primary) and the transcript (secondary).
2. Pay **special attention** to technical knowledge, skills, tools, environments, and examples. This is **extremely important** – include as much technical detail and depth as possible.
3. Follow the structure provided in this format template:
{mall_text}
4. Use the tone, language, and structure of this style reference:
{style_text}

📌 Important guidelines:
- Begin with a **bullet point list** containing key facts (e.g. skills, goals, salary expectations, availability).
- The summary must be **as detailed as possible**, based only on the information in the files.
- Write in a **chronological, reflective and concrete** style – just like a recruiter describing a candidate.
- Avoid bullet points in the main body (unless the template specifically uses them).
- Use a **professional but relaxed** tone – it should sound like it was written by a person.

🛠️ Formatting:
- Add **double asterisks** before and after all headings (e.g. **General**, **Technical skills**, etc.).
- Leave one empty line before each heading.

🚫 Limitations:
You may not invent, guess, or add any information that cannot be clearly derived from the interview notes or transcript. All content must be directly based on what is written above.
"""