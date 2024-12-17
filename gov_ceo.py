# # gov_ceo.py
# import openai
# import streamlit as st
#
# openai.api_key = st.secrets["OPENAI_API_KEY"]
#
# def generate_solution(sector, department, concern):
#     system_prompt = f"You are the chief executive of the {department}. Provide a concise, actionable solution."
#     user_prompt = f"""
#     Concern: {concern}
#     Sector: {sector}
#
#     Provide a short action plan to address this concern. Be direct and authoritative.
#     """
#
#     try:
#         # No client instantiation needed, just call openai.ChatCompletion directly:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "system", "content": system_prompt},
#                 {"role": "user", "content": user_prompt}
#             ],
#             temperature=0.5
#         )
#         solution = response.choices[0].message.content.strip()
#         return solution
#     except Exception as e:
#         st.error(f"Error generating solution: {str(e)}")
#         return f"Unable to generate solution: {str(e)}"

# gov_ceo.py
import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_solution(sector, department, concern):
    system_prompt = f"You are the chief executive of the {department}. Provide a concise, actionable solution."
    user_prompt = f"""
    Concern: {concern}
    Sector: {sector}

    Provide a short action plan to address this concern. Be direct and authoritative.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5
        )
        solution = response.choices[0].message.content.strip()
        return solution
    except Exception as e:
        st.error(f"Error generating solution: {str(e)}")
        return f"Unable to generate solution: {str(e)}"
