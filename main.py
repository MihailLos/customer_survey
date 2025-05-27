from PIL import Image
import streamlit as st
import base64
from io import BytesIO
import load_data

st.set_page_config(page_title="Опрос о маркировке пищевой продукции", layout="centered")

maxdiff_has_error = False
required_question_check = False

def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

kemsu_logo = Image.open("kemsu_logo.png")
st.markdown(
    """
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <img src="data:image/png;base64,%s" style="height: 120px;">
    </div>
    """ % image_to_base64(kemsu_logo),
    unsafe_allow_html=True
)

# Состояние страницы
if "page" not in st.session_state:
    st.session_state.page = 0

TOTAL_PAGES = 28
current_page = st.session_state.page
progress = int((current_page / (TOTAL_PAGES - 1)) * 100)

st.progress(progress)
st.markdown(f"**Прогресс прохождения опроса: {progress}%**")

# Навигация
def go_next():
    st.session_state.page += 1

# Проверка обязательного выбора radio
def check_required_question(id):
    if st.session_state.get(id) is None:
        st.error("❌ Выберите один вариант ответа для продолжения опроса.")
        return True
    else:
        return False

# Проверка для MaxDiff: нельзя одинаковые варианты
def check_maxdiff_question(id1, id2):
    v1 = st.session_state.get(id1)
    v2 = st.session_state.get(id2)
    if v1 is None or v2 is None:
        st.error("❌ Выберите варианты ответа для продолжения опроса.")
        return True
    elif v1 == v2:
        st.error("❌ Нельзя выбирать один и тот же вариант как наиболее и наименее важный.")
        return True
    else:
        return False


# Проверка поля "Другое" — если выбрано, нужно заполнить
def check_other_required(select_id, text_id):
    selected = st.session_state.get(select_id)
    other_text = st.session_state.get(text_id)
    print(type(selected))
    if selected is None:
        st.error("❌ Выберите один вариант ответа для продолжения опроса.")
        return True
    elif len(selected) == 0:
        st.error("❌ Выберите один или более вариантов ответа для продолжения опроса.")
        return True
    elif "Другое" in selected and (not other_text):
        st.error("❌ Заполните поле 'Другое'.")
        return True
    else:
        return False

# --- Страница 0: Приветствие ---
if st.session_state.page == 0:
    st.title("Добро пожаловать в опрос!")
    st.markdown("#### Исследование потребительских предпочтений при выборе пищевой продукции")
    st.markdown("**Цель опроса** — выявление ключевых факторов, определяющих потребительский выбор при покупке пищевой продукции.")
    st.markdown("Опрос займет не более 10 минут. Ваши ответы анонимны и будут использованы исключительно в исследовательских целях.")
    st.button("Начать опрос", on_click=go_next)

# --- Страница 1: Вопросы 1–3 ---
elif st.session_state.page == 1:
    st.markdown("### Вопрос 1. Как часто Вы покупаете пищевую продукцию?")
    selected = st.radio("", ["Каждый день", "Несколько раз в неделю", "Один раз в неделю", "Реже одного раза в неделю"], index=None)
    st.session_state["q1"] = selected
    st.button("Далее", on_click=go_next, disabled=check_required_question("q1"))

elif st.session_state.page == 2:
    st.markdown("### Вопрос 2. Где чаще всего Вы приобретаете пищевую продукцию? (возможно указать несколько вариантов ответа)")
    selected = []
    for option in ["Супермаркеты", "Магазины 'у дома'", "Ларьки/киоски", "Рынки", "Онлайн-сервисы доставки", "Другое"]:
        if st.checkbox(option, key=f"q2_{option}"):
            selected.append(option)
    st.session_state["q2"] = selected
    if "Другое" in selected:
        st.text_input("Напишите свой вариант:", key="q2_other")
    st.button("Далее", on_click=go_next, disabled=check_other_required("q2", "q2_other"))

elif st.session_state.page == 3:
    st.markdown("### Вопрос 3. Напишите, какие 3 элемента маркировки, по Вашему мнению, должны быть выделены наиболее заметно на упаковке любой пищевой продукции?")
    e1 = st.text_input("Элемент 1:")
    st.session_state["q3_1"] = e1
    e2 = st.text_input("Элемент 2:")
    st.session_state["q3_2"] = e2
    e3 = st.text_input("Элемент 3:")
    st.session_state["q3_3"] = e3
    st.button("Далее", on_click=go_next, disabled=not all([e1, e2, e3]))

# MaxDiff пример — Вопрос 4
elif st.session_state.page == 4:
    st.markdown("### Вопрос 4. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Рекомендации и/или ограничения по использованию (в том числе по приготовлению)", 
                   "Количество (или объем) пищевой продукции", "Условия хранения", "Дата изготовления"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m1"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l1"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m1", "l1"))

elif st.session_state.page == 5:
    st.markdown("### Вопрос 5. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Состав", "Срок годности", "Пищевая ценность (содержание или отсутствие определённых веществ)", 
                "Наличие единого знака обращения продукции на рынке Евразийского экономического союза (EAC)"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m2"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l2"] = sel1
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m2", "l2"))

elif st.session_state.page == 6:
    st.markdown("### Вопрос 6. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Наличие единого знака обращения продукции на рынке Евразийского экономического союза (EAC)", "Состав", 
                   "Наименование и местонахождение изготовителя", 
                   "Рекомендации и/или ограничения по использованию (в том числе по приготовлению)"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m3"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l3"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m3", "l3"))

elif st.session_state.page == 7:
    st.markdown("### Вопрос 7. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Наименование и местонахождение изготовителя", "Условия хранения", "Срок годности", 
                   "Пищевая ценность (содержание или отсутствие определённых веществ)"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m4"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l4"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m4", "l4"))

elif st.session_state.page == 8:
    st.markdown("### Вопрос 8. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Дата изготовления", 
                   "Наличие единого знака обращения продукции на рынке Евразийского экономического союза (EAC)", 
                   "Состав", "Условия хранения"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m5"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l5"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m5", "l5"))

elif st.session_state.page == 9:
    st.markdown("### Вопрос 9. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Пищевая ценность (содержание или отсутствие определённых веществ)", "Дата изготовления", 
                   "Рекомендации и/или ограничения по использованию (в том числе по приготовлению)", "Срок годности"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m6"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l6"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m6", "l6"))

elif st.session_state.page == 10:
    st.markdown("### Вопрос 10. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Срок годности", "Наименование и местонахождение изготовителя", "Количество (или объем) пищевой продукции", 
                   "Состав"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m7"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l7"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m7", "l7"))

elif st.session_state.page == 11:
    st.markdown("### Вопрос 11. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Количество (или объем) пищевой продукции", 
                   "Пищевая ценность (содержание или отсутствие определённых пищевых веществ)", 
                   "Дата изготовления", "Наименование и местонахождение изготовителя"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m8"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l8"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m8", "l8"))

elif st.session_state.page == 12:
    st.markdown("### Вопрос 12. При выборе продукции, какая информация на маркировке наиболее важна и наименее важна для Вас?")
    with st.container():
        options = ["Условия хранения", "Рекомендации и/или ограничения по использованию (в том числе по приготовлению)", 
                   "Наличие единого знака обращения продукции на рынке Евразийского экономического союза (EAC)", 
                   "Количество (или объем) пищевой продукции"]
        st.markdown('<div style="background-color:#e6f4ea;padding:10px;border-radius:5px;"><b>Наиболее важная информация</b></div>', unsafe_allow_html=True)
        sel1 = st.radio("", options, index=None)
        st.session_state["m9"] = sel1
        st.markdown('<div style="background-color:#fdecea;padding:10px;border-radius:5px;"><b>Наименее важная информация</b></div>', unsafe_allow_html=True)
        sel2 = st.radio("", options, index=None)
        st.session_state["l9"] = sel2
        st.button("Далее", on_click=go_next, disabled=check_maxdiff_question("m9", "l9"))

# --- Страница 3: Вопросы 13–19 ---
elif st.session_state.page == 13:
    st.markdown("### Вопрос 13. Насколько Вы осведомлены о содержании нутриентов (белков, жиров, углеводов, витаминов и др.) в продукции, которую покупаете?")
    select = st.radio("", ["Хорошо ориентируюсь", "Частично понимаю", "Знаю общие принципы", "Не обращаю внимания"], index=None)
    st.session_state["q13"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q13"))

elif st.session_state.page == 14:
    st.markdown("### Вопрос 14. Насколько для Вас важна информация о пользе продукции для здоровья (например, содержание соли, сахара, холестерина)?")
    select = st.radio("", ["Очень важно", "Скорее важно", "Не имеет значения"], index=None)
    st.session_state["q14"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q14"))

elif st.session_state.page == 15:
    st.markdown("### Вопрос 15. Часто ли Вы сталкиваетесь с трудностями при покупке продукции (например, мелкий шрифт на упаковке)?")
    select = st.radio("", ["Да, регулярно", "Иногда", "Нет"], index=None)
    st.session_state["q15"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q15"))

elif st.session_state.page == 16:
    st.markdown("### Вопрос 16. Обращаете ли Вы внимание на наличие специализированной пищевой продукции (например, с пониженным содержанием сахара, безглютеновых, гипоаллергенных и др.)?")
    select = st.radio("", ["Да, это важно", "Иногда обращаю внимание", "Нет, не обращаю внимание"], index=None)
    st.session_state["q16"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q16"))

elif st.session_state.page == 17:
    st.markdown("### Вопрос 17. Какой информацией Вы хотели бы пользоваться при выборе продукции? (можно выбрать несколько вариантов)")
    selected = []
    for option in ["Рейтинги качества", "Сравнение цен в разных магазинах", "Подробный анализ состава", 
                   "Отзывы других покупателей", "Рекомендации по здоровому питанию", "Другое"]:
        if st.checkbox(option, key=f"q17_{option}"):
            selected.append(option)
    st.session_state["q17"] = selected
    if "Другое" in selected:
        st.text_input("Напишите свой вариант:", key="q17_other")
    st.button("Далее", on_click=go_next, disabled=check_other_required("q17", "q17_other"))

elif st.session_state.page == 18:
    st.markdown("### Вопрос 18. Читаете ли Вы информацию на упаковке перед покупкой?")
    select = st.radio("", ["Да, всегда внимательно изучаю", "Смотрю, но не углубляюсь", 
              "Читаю только при выборе новой продукции", "Нет, не обращаю внимания"], index=None)
    st.session_state["q18"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q18"))

elif st.session_state.page == 19:
    st.markdown("### Вопрос 19. Хотели бы вы пользоваться цифровой системой, которая помогает выбирать пищевую продукцию на основе ваших предпочтений?")
    select = st.radio("", ["Да", "Нет", "Затрудняюсь ответить"], index=None)
    st.session_state["q19"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q19"))

# --- Страница 4: Социально-демографический блок (20–27) ---
elif st.session_state.page == 20:
    st.markdown("### Вопрос 20. Ваш пол")
    select = st.radio("", ["Мужской", "Женский"], index=None)
    st.session_state["q20"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q20"))

elif st.session_state.page == 21:
    st.markdown("### Вопрос 21. Ваша возрастная категория")
    select = st.radio("", ["18–29 лет", "30–39 лет", "40–49 лет", "50–59 лет", "60 лет и выше"], index=None)
    st.session_state["q21"] = select
    st.button("Далее", on_click=go_next, disabled=check_required_question("q21"))

elif st.session_state.page == 22:
    st.markdown("### Вопрос 22. Ваше образование (на текущий момент)")
    selected = st.radio("", ["Школа", "Неоконченное среднее специальное", "Колледж / техникум", "Неоконченное высшее",
              "Бакалавриат / специалитет", "Магистратура / аспирантура", "Другое"], key="q22", index=None)
    if selected == "Другое":
        st.text_input("Уточните ваше образование:", key="q22_other")
    st.button("Далее", on_click=go_next, disabled=check_other_required("q22", "q22_other"))

elif st.session_state.page == 23:
    st.markdown("### Вопрос 23. Ваш род занятий")
    selected = st.radio("", ["Учащийся / студент", "Работающий (наёмный)", "Работающий (Самозанятый / предприниматель)",
              "Пенсионер", "Безработный", "Другое"], index=None)
    st.session_state["q23"] = selected
    if selected == "Другое":
        text = st.text_input("Уточните ваш род занятий:")
        st.session_state["q23_other"] = text
    st.button("Далее", on_click=go_next, disabled=check_other_required("q23", "q23_other"))

elif st.session_state.page == 24:
    st.markdown("### Вопрос 24. Ваше семейное положение")
    selected = st.radio("", ["Состою в браке", "Не состою в браке"], index=None)
    st.session_state["q24"] = selected
    st.button("Далее", on_click=go_next, disabled=check_required_question("q24"))

elif st.session_state.page == 25:
    st.markdown("### Вопрос 25. Сколько человек проживает с Вами?")
    selected = st.radio("", ["Живу один", "1 человек", "2 человека", "3 человека", "4 человека", "5 и более"], index=None)
    st.session_state["q25"] = selected
    st.button("Далее", on_click=go_next, disabled=check_required_question("q25"))

elif st.session_state.page == 26:
    st.markdown("### 26. Насколько комфортно Вам покрывать расходы на питание?")
    selected = st.radio("", ["Очень комфортно (не экономлю)", "Достаточно комфортно (иногда ищу скидки)", 
                  "Затруднительно (часто выбираю бюджетные варианты)", 
                  "Очень сложно (вынужден(-а) сильно экономить на пищевой продукции)"], index=None)
    st.session_state["q26"] = selected
    st.button("Далее", on_click=go_next, disabled=check_required_question("q26"))

elif st.session_state.page == 27:
    st.markdown("### 27. Есть ли у Вас дети до 18 лет?")
    selected = st.radio("", ["Да", "Нет"], index=None)
    st.session_state["q27"] = selected

    if st.button("Отправить анкету", disabled=check_required_question("q27")):
        answers = load_data.build_answers()

        st.write("Ответы, отправляемые в Airtable:")
        st.json(answers)

        load_data.send_to_airtable(answers)
        st.success("Спасибо за участие в опросе! Ваши ответы сохранены.")
