import streamlit as st

st.set_page_config(page_title="Опрос о маркировке пищевой продукции", layout="centered")

if "page" not in st.session_state:
    st.session_state.page = 0

def go_next():
    st.session_state.page += 1

def go_back():
    st.session_state.page -= 1

# --- Страница 0: Приветствие ---
if st.session_state.page == 0:
    st.title("Добро пожаловать в опрос!")
    st.markdown("#### Исследование потребительских предпочтений при выборе пищевой продукции")
    st.markdown("**Цель опроса** — выявить ключевые факторы, влияющие на выбор продуктов питания на основе маркировки.")
    st.markdown("Опрос займет не более 5–7 минут. Ваши ответы анонимны и будут использованы исключительно в исследовательских целях.")
    st.button("Начать опрос", on_click=go_next)

# --- Страница 1: Вопросы 1–3 ---
elif st.session_state.page == 1:
    st.header("Блок 2. Вопросы о потребительском поведении")

    st.radio("1. Как часто Вы покупаете пищевую продукцию?", 
             ["Каждый день", "Несколько раз в неделю", "Один раз в неделю", "Реже одного раза в неделю"], key="q1")

    st.markdown("2. Где чаще всего Вы приобретаете пищевую продукцию? (можно выбрать несколько вариантов)")
    q2_selected = []
    for option in ["Супермаркеты", "Магазины 'у дома'", "Ларьки/киоски", "Рынки", "Онлайн-сервисы доставки", "Другое"]:
        if st.checkbox(option, key=f"q2_{option}"):
            q2_selected.append(option)
    if "Другое" in q2_selected:
        st.text_input("Уточните, что вы имели в виду под 'Другое':", key="q2_other")

    st.markdown("3. Напишите, какие 3 элемента маркировки, по Вашему мнению, должны быть выделены наиболее заметно на упаковке любой пищевой продукции?")
    st.text_input("Элемент 1:", key="q3_1")
    st.text_input("Элемент 2:", key="q3_2")
    st.text_input("Элемент 3:", key="q3_3")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Назад", on_click=go_back)
    with col2:
        st.button("Далее", on_click=go_next)

# --- Страница 2: Вопросы 4–12 (MaxDiff) ---
elif st.session_state.page == 2:
    st.header("Блок 2. MaxDiff: важность информации на упаковке")

    maxdiff_has_error = False

    st.markdown("### Вопрос 4")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m1 = st.radio("", ["Рекомендации и/или ограничения по использованию",
                           "Количество (или объем) пищевой продукции",
                           "Условия хранения",
                           "Дата изготовления"], key="m1")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l1 = st.radio("", ["Рекомендации и/или ограничения по использованию",
                           "Количество (или объем) пищевой продукции",
                           "Условия хранения",
                           "Дата изготовления"], key="l1")
    st.markdown("---")
    if st.session_state.get("m1") == st.session_state.get("l1"):
        st.warning("⚠️ Вопрос 4: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 5")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m2 = st.radio("", [
        "Состав",
        "Срок годности",
        "Пищевая ценность (содержание или отсутствие определённых веществ)",
        "Наличие знака обращения на рынке ЕАЭС (EAC)"
    ], key="m2")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l2 = st.radio("", [
        "Состав",
        "Срок годности",
        "Пищевая ценность (содержание или отсутствие определённых веществ)",
        "Наличие знака обращения на рынке ЕАЭС (EAC)"
    ], key="l2")
    st.markdown("---")
    if st.session_state.get("m2") == st.session_state.get("l2"):
        st.warning("⚠️ Вопрос 5: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 6")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m3 = st.radio("", [
        "Наличие знака обращения на рынке ЕАЭС (EAC)",
        "Состав",
        "Наименование и местонахождение изготовителя",
        "Рекомендации и/или ограничения по использованию"
    ], key="m3")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l3 = st.radio("", [
        "Наличие знака обращения на рынке ЕАЭС (EAC)",
        "Состав",
        "Наименование и местонахождение изготовителя",
        "Рекомендации и/или ограничения по использованию"
    ], key="l3")
    st.markdown("---")
    if st.session_state.get("m3") == st.session_state.get("l3"):
        st.warning("⚠️ Вопрос 6: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 7")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m4 = st.radio("", [
        "Наименование и местонахождение изготовителя",
        "Условия хранения",
        "Срок годности",
        "Пищевая ценность (содержание или отсутствие определённых веществ)"
    ], key="m4")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l4 = st.radio("", [
        "Наименование и местонахождение изготовителя",
        "Условия хранения",
        "Срок годности",
        "Пищевая ценность (содержание или отсутствие определённых веществ)"
    ], key="l4")
    st.markdown("---")
    if st.session_state.get("m4") == st.session_state.get("l4"):
        st.warning("⚠️ Вопрос 7: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 8")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m5 = st.radio("", [
        "Дата изготовления",
        "Наличие знака обращения на рынке ЕАЭС (EAC)",
        "Состав",
        "Условия хранения"
    ], key="m5")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l5 = st.radio("", [
        "Дата изготовления",
        "Наличие знака обращения на рынке ЕАЭС (EAC)",
        "Состав",
        "Условия хранения"
    ], key="l5")
    st.markdown("---")
    if st.session_state.get("m5") == st.session_state.get("l5"):
        st.warning("⚠️ Вопрос 8: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 9")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m6 = st.radio("", [
        "Пищевая ценность (содержание или отсутствие определённых веществ)",
        "Дата изготовления",
        "Рекомендации и/или ограничения по использованию",
        "Срок годности"
    ], key="m6")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l6 = st.radio("", [
        "Пищевая ценность (содержание или отсутствие определённых веществ)",
        "Дата изготовления",
        "Рекомендации и/или ограничения по использованию",
        "Срок годности"
    ], key="l6")
    st.markdown("---")
    if st.session_state.get("m6") == st.session_state.get("l6"):
        st.warning("⚠️ Вопрос 9: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 10")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m7 = st.radio("", [
        "Срок годности",
        "Наименование и местонахождение изготовителя",
        "Количество (или объем) пищевой продукции",
        "Состав"
    ], key="m7")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l7 = st.radio("", [
        "Срок годности",
        "Наименование и местонахождение изготовителя",
        "Количество (или объем) пищевой продукции",
        "Состав"
    ], key="l7")
    st.markdown("---")
    if st.session_state.get("m7") == st.session_state.get("l7"):
        st.warning("⚠️ Вопрос 10: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 11")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m8 = st.radio("", [
        "Количество (или объем) пищевой продукции",
        "Пищевая ценность (содержание или отсутствие определённых веществ)",
        "Дата изготовления",
        "Наименование и местонахождение изготовителя"
    ], key="m8")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l8 = st.radio("", [
        "Количество (или объем) пищевой продукции",
        "Пищевая ценность (содержание или отсутствие определённых веществ)",
        "Дата изготовления",
        "Наименование и местонахождение изготовителя"
    ], key="l8")
    st.markdown("---")
    if st.session_state.get("m8") == st.session_state.get("l8"):
        st.warning("⚠️ Вопрос 11: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    st.markdown("### Вопрос 12")
    with st.container():
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        m9 = st.radio("", [
        "Условия хранения",
        "Рекомендации и/или ограничения по использованию",
        "Наличие знака обращения на рынке ЕАЭС (EAC)",
        "Количество (или объем) пищевой продукции"
    ], key="m9")
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        l9 = st.radio("", [
        "Условия хранения",
        "Рекомендации и/или ограничения по использованию",
        "Наличие знака обращения на рынке ЕАЭС (EAC)",
        "Количество (или объем) пищевой продукции"
    ], key="l9")
    st.markdown("---")
    if st.session_state.get("m9") == st.session_state.get("l9"):
        st.warning("⚠️ Вопрос 12: Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        maxdiff_has_error = True

    col1, col2 = st.columns(2)
    with col1:
        st.button("Назад", on_click=go_back)
    with col2:
        st.button("Далее", on_click=go_next, disabled=maxdiff_has_error)

# --- Страница 3: Вопросы 13–19 ---
elif st.session_state.page == 3:
    st.header("Блок 2. Дополнительные поведенческие вопросы")

    st.radio("13. Насколько Вы осведомлены о содержании нутриентов?",
             ["Хорошо ориентируюсь", "Частично понимаю", "Знаю общие принципы", "Не обращаю внимания"], key="q13")

    st.radio("14. Насколько для Вас важна информация о пользе продукции для здоровья?",
             ["Очень важно", "Скорее важно", "Не имеет значения"], key="q14")

    st.radio("15. Часто ли Вы сталкиваетесь с трудностями при покупке продукции?",
             ["Да, регулярно", "Иногда", "Нет"], key="q15")

    st.radio("16. Обращаете ли Вы внимание на специализированную продукцию?",
             ["Да, это важно", "Иногда обращаю внимание", "Нет, не обращаю внимание"], key="q16")

    st.markdown("17. Какой информацией Вы хотели бы пользоваться при выборе продукции? (можно выбрать несколько вариантов)")
    q17_selected = []
    for option in ["Рейтинги качества", "Сравнение цен", "Анализ состава", "Отзывы", "Рекомендации по здоровому питанию", "Другое"]:
        if st.checkbox(option, key=f"q17_{option}"):
            q17_selected.append(option)
    if "Другое" in q17_selected:
        st.text_input("Уточните, что вы имели в виду под 'Другое':", key="q17_other")

    st.radio("18. Читаете ли Вы информацию на упаковке перед покупкой?",
             ["Всегда внимательно изучаю", "Смотрю, но не углубляюсь", 
              "Читаю только при выборе новой продукции", "Не обращаю внимания"], key="q18")

    st.radio("19. Хотели бы вы пользоваться цифровой системой подбора продукции?",
             ["Да", "Нет", "Затрудняюсь ответить"], key="q19")

    col1, col2 = st.columns(2)
    with col1:
        st.button("Назад", on_click=go_back)
    with col2:
        st.button("Далее", on_click=go_next)

# --- Страница 4: Социально-демографический блок (20–27) ---
elif st.session_state.page == 4:
    st.header("Блок 3. Социально-демографический")

    st.radio("20. Пол", ["Мужской", "Женский"], key="q20")
    st.radio("21. Возрастная категория", ["18–29 лет", "30–39 лет", "40–49 лет", "50–59 лет", "60 лет и выше"], key="q21")

    q22_value = st.radio("22. Образование", 
             ["Школа", "Неоконченное среднее специальное", "Колледж / техникум", "Неоконченное высшее",
              "Бакалавриат / специалитет", "Магистратура / аспирантура", "Другое"], key="q22")
    if q22_value == "Другое":
        st.text_input("Уточните ваше образование:", key="q22_other")

    q23_value = st.radio("23. Род занятий", 
             ["Учащийся / студент", "Работающий (наёмный)", "Самозанятый / предприниматель",
              "Пенсионер", "Безработный", "Другое"], key="q23")
    if q23_value == "Другое":
        st.text_input("Уточните ваш род занятий:", key="q23_other")

    st.radio("24. Семейное положение", ["Состою в браке", "Не состою в браке"], key="q24")
    st.radio("25. Сколько человек проживает с Вами?", 
             ["Один", "1 человек", "2 человека", "3 человека", "4 человека", "5 и более"], key="q25")
    st.radio("26. Насколько комфортно Вам покрывать расходы на питание?",
             ["Очень комфортно", "Достаточно комфортно", "Затруднительно", "Очень сложно"], key="q26")
    st.radio("27. Есть ли у вас дети до 18 лет?", ["Да", "Нет"], key="q27")

    if st.button("Отправить анкету"):
        st.success("Спасибо за участие в опросе! Ваши ответы сохранены.")

    st.button("Назад", on_click=go_back)
