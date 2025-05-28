import streamlit as st
import load_data

def single_choice_question(form_key, question_key, question_text, options):
    answer_key = f"{form_key}_answer"

    def onclick():
        answer = st.session_state.get(answer_key)
        if not answer:
            st.session_state["form_error"] = "❌ Выберите один вариант ответа."
        else:
            st.session_state[question_key] = answer
            st.session_state["form_error"] = ""
            st.session_state.page += 1

    with st.form(form_key):
        st.markdown(f"### {question_text}")
        st.radio("", options, index=None, key=answer_key)
        st.form_submit_button("Далее", on_click=onclick)

    # Отображаем ошибку после формы
    if st.session_state.get("form_error"):
        st.error(st.session_state["form_error"])

def single_choice_with_other(form_key, question_key, question_text, options, other_key):
    answer_key = f"{form_key}_{question_key}"
    other_input_key = f"{form_key}_{other_key}_input"

    def validate_answer():
        answer = st.session_state.get(answer_key)
        other_text = st.session_state.get(other_input_key, "")
        if not answer:
            st.session_state["form_error"] = "❌ Выберите один вариант ответа."
        elif answer == "Другое" and not other_text:
            st.session_state["form_error"] = "❌ Уточните вариант 'Другое'."
        else:
            st.session_state[question_key] = answer
            st.session_state[other_key] = other_text
            st.session_state["form_error"] = ""
            st.session_state.page += 1

    with st.form(form_key):
        st.markdown(f"### {question_text}")
        st.radio("", options + ["Другое"], index=None, key=answer_key)
        if st.session_state.get(answer_key) == "Другое":
            st.text_input("Уточните:", key=other_input_key)
        st.form_submit_button("Далее", on_click=validate_answer)

    if st.session_state.get("form_error"):
        st.error(st.session_state["form_error"])


def multiple_choice_with_other(form_key, question_key, question_text, options, other_key):
    selection_key = f"{form_key}_{question_key}"
    other_input_key = f"{form_key}_{other_key}_input"

    def validate_answer():
        selected = [opt for opt in options + ["Другое"] if st.session_state.get(f"{form_key}_{question_key}_{opt}")]
        other_text = st.session_state.get(other_input_key, "")
        if not selected:
            st.session_state["form_error"] = "❌ Выберите хотя бы один вариант."
        elif "Другое" in selected and not other_text:
            st.session_state["form_error"] = "❌ Уточните вариант 'Другое'."
        else:
            st.session_state[question_key] = selected
            st.session_state[other_key] = other_text
            st.session_state["form_error"] = ""
            st.session_state.page += 1

    with st.form(form_key):
        st.markdown(f"### {question_text}")
        for option in options + ["Другое"]:
            st.checkbox(option, key=f"{form_key}_{question_key}_{option}")
        if st.session_state.get(f"{form_key}_{question_key}_Другое"):
            st.text_input("Уточните:", key=other_input_key)
        st.form_submit_button("Далее", on_click=validate_answer)

    if st.session_state.get("form_error"):
        st.error(st.session_state["form_error"])


def triple_text_input(form_key, question_key_prefix, question_text, options):
    input_keys = [f"{form_key}_{question_key_prefix}_{i}" for i in range(1, len(options) + 1)]

    def validate_answer():
        values = [st.session_state.get(k, "") for k in input_keys]
        if not all(values):
            st.session_state["form_error"] = "❌ Заполните все поля."
        else:
            for i, val in enumerate(values, start=1):
                st.session_state[f"{question_key_prefix}_{i}"] = val
            st.session_state["form_error"] = ""
            st.session_state.page += 1

    with st.form(form_key):
        st.markdown(f"### {question_text}")
        for i, text in enumerate(options, start=1):
            st.text_input(text, key=input_keys[i - 1])
        st.form_submit_button("Далее", on_click=validate_answer)

    if st.session_state.get("form_error"):
        st.error(st.session_state["form_error"])


def maxdiff_question_visual(form_key, question_index, question_text, options):
    most_key = f"m{question_index}"
    least_key = f"l{question_index}"

    def validate_answer():
        most = st.session_state.get(most_key)
        least = st.session_state.get(least_key)
        if not most or not least:
            st.session_state["form_error"] = "❌ Выберите оба варианта."
        elif most == least:
            st.session_state["form_error"] = "❌ Нельзя выбирать один и тот же вариант как наиболее и наименее важный."
        else:
            st.session_state["form_error"] = ""
            st.session_state.page += 1

    with st.form(form_key):
        st.markdown(f"### {question_text}")
        st.markdown(
            """
            <style>
            .maxdiff-table td {
                padding: 6px 12px;
                text-align: center;
                vertical-align: middle;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Заголовки
        col1, col2, col3 = st.columns([1, 4, 1])
        with col1:
            st.markdown("**Наиболее важный**")
        with col2:
            st.markdown(" ")
        with col3:
            st.markdown("**Наименее важный**")

        # Отображение строк с вариантами
        for i, opt in enumerate(options):
            col1, col2, col3 = st.columns([1, 4, 1])
            with col1:
                if st.radio("", [" "], key=f"{form_key}_most_{i}") == " ":
                    st.session_state[most_key] = opt
            with col2:
                st.markdown(f"<div style='text-align:center;'>{opt}</div>", unsafe_allow_html=True)
            with col3:
                if st.radio("", [" "], key=f"{form_key}_least_{i}") == " ":
                    st.session_state[least_key] = opt

        st.form_submit_button("Далее", on_click=validate_answer)

    if st.session_state.get("form_error"):
        st.error(st.session_state["form_error"])

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