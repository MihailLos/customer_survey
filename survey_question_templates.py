import streamlit as st
import load_data

def single_choice_question(form_key, question_key, question_text, options):
    def onclick():
        st.session_state[question_key] = answer
        st.session_state.page += 1
    def validate_answer(answer):
        if not answer:
                st.error("❌ Выберите один вариант ответа.")
                return True
            
    with st.form(form_key, enter_to_submit=True):
        st.markdown(f"### {question_text}")
        answer = st.radio("", options, index=None)
        st.form_submit_button("Далее", on_click=onclick, disabled=validate_answer)

def single_choice_with_other(form_key, question_key, question_text, options, other_key):
    def validate_answer():
        if not answer:
            st.error("❌ Выберите один вариант ответа.")
        elif answer == "Другое" and not other_text:
            st.error("❌ Уточните вариант 'Другое'.")
        else:
            st.session_state[question_key] = answer
            st.session_state[other_key] = other_text
            st.session_state.page += 1

    with st.form(form_key, enter_to_submit=True):
        st.markdown(f"### {question_text}")
        answer = st.radio("", options + ["Другое"], index=None)
        other_text = ""
        if answer == "Другое":
            other_text = st.text_input("Уточните:")
        st.form_submit_button("Далее", on_click=validate_answer)

def multiple_choice_with_other(form_key, question_key, question_text, options, other_key):
    def validate_answer():
        if not selected:
            st.error("❌ Выберите хотя бы один вариант.")
        elif "Другое" in selected and not other_text:
            st.error("❌ Уточните вариант 'Другое'.")
        else:
            st.session_state[question_key] = selected
            st.session_state[other_key] = other_text
            st.session_state.page += 1

    with st.form(form_key, enter_to_submit=True):
        st.markdown(f"### {question_text}")
        selected = []
        for option in options + ["Другое"]:
            if st.checkbox(option, key=f"{question_key}_{option}"):
                selected.append(option)
        other_text = ""
        if "Другое" in selected:
            other_text = st.text_input("Уточните:")
        st.form_submit_button("Далее", on_click=validate_answer)
            
def triple_text_input(form_key, question_key_prefix, question_text, options):
    def validate_answer():
        if not all(answers):
            st.error("❌ Заполните все поля.")
        else:
            for i, ans in enumerate(answers, start=1):
                st.session_state[f"{question_key_prefix}_{i}"] = ans
            st.session_state.page += 1
    with st.form(form_key, enter_to_submit=True):
        st.markdown(f"### {question_text}")
        answers = [st.text_input(text) for text in options]
        st.form_submit_button("Далее", on_click=validate_answer)

import streamlit as st

def maxdiff_question(form_key, question_index, question_text, options):
    def validate_answer():
        if not most or not least:
            st.error("❌ Выберите оба варианта.")
        elif most == least:
            st.error("❌ Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        else:
            st.session_state[f"m{question_index}"] = most
            st.session_state[f"l{question_index}"] = least
            st.session_state.page += 1

    with st.form(form_key, enter_to_submit=True):
        st.markdown(f"### {question_text}")
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        most = st.radio("", options, index=None, key=f"max_{question_index}")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        least = st.radio("", options, index=None, key=f"min_{question_index}")
        st.form_submit_button("Далее", on_click=validate_answer)

def final_submit_screen(form_key="form_submit"):
    with st.form(form_key, enter_to_submit=True):
        st.markdown("### Спасибо за участие в опросе!")
        st.markdown("Пожалуйста, нажмите кнопку ниже, чтобы отправить свои ответы.")
        submitted = st.form_submit_button("Отправить анкету")
        if submitted:
            answers = load_data.build_answers()
            st.write("Ответы, отправляемые в Airtable:")
            st.json(answers)
            load_data.send_to_airtable(answers)
            st.success("✅ Ваши ответы успешно отправлены. Спасибо за участие!")