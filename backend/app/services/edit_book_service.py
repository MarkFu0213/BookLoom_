from openai import OpenAI, OpenAIError
from mappers.edit_book_mapper import get_book_by_serial, update_book_text
from config import OPENAI_API_KEY

MODEL="gpt-4o"

def edit_book_service(book_serial, editing_option):
    # Retrieve the book's existing text
    book = get_book_by_serial(book_serial)
    if not book:
        return None

    client = OpenAI(
        api_key=OPENAI_API_KEY,  # This is the default and can be omitted
    )
    # Prepare the prompt for the OpenAI API based on the editing option
    prompt = f"Rewrite the following text in a {editing_option} style. text```\n{book['text']}```"

    try:
        # Call OpenAI API to get the rewritten text

        completion = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": "You are a creative writing assistant."},
                # <-- This is the system message that provides context to the model
                {"role": "user", "content": prompt}
                # <-- This is the user message for which the model will generate a response
            ],
            max_tokens=2048,
            temperature=0.7
        )



        # Extract the generated text
        updated_text = completion.choices[0].message.content

        # Update the text in the database via the mapper
        update_success = update_book_text(book_serial, updated_text)
        return updated_text if update_success else None

    except OpenAIError as e:
        print(f"OpenAI API Error: {str(e)}")
        return None
