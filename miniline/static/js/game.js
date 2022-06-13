function GameSession() {
    this.points = 0
    this.click_power = 1
    this.auto_click_power = 0
    this.next_level_price = 10
    this.task_text = "Error!"
    this.words = []
    this.loaded_words = []


    this.init = function () {
        getCore().then(core => {
            this.points = core.points
            this.click_power = core.click_power
            this.auto_click_power = core.auto_click_power
            this.next_level_price = core.next_level_price
            this.words = core.words.split(/\r?\n?\s+/)
            let lang_indicator = document.getElementById("lang-indicator")
            if (core.lang === "")
                lang_indicator.innerText = "мой";
            else
                lang_indicator.innerText = core.lang === "ru" ? "ru" : "en";
            this.task_text = generate_task()
            render()
        })
    }

    this.add_points = function (points) {
        this.points += points
        this.check_levelup()
        render()
    }

    this.add_power = function (power) {
        this.click_power += power
        render()
    }

    this.add_auto_power = function (power) {
        this.auto_click_power += power
        render()
    }

    this.check_levelup = function () {
        if (this.points >= this.next_level_price) {
            updatePoints(this.points).then(core => {
                this.next_level_price = core.next_level_price
            })
        }
    }

    this.update_task = function () {
        this.task_text = generate_task()
        render()
    }
}

let Game = new GameSession() // Экземпляр класса GameSession.


function generate_task() {
    let word = Game.words[Math.floor(Math.random() * Game.words.length)]
    while (word === "" || word === "\n" || word === "\r" || word === " ") {
        word = Game.words[Math.floor(Math.random() * Game.words.length)]
    }
    return word
}

function render() {
    const pointsNode = document.getElementById('points')
    const clickNode = document.getElementById('click_power')
    const autoClickNode = document.getElementById('auto_click_power')
    const taskTextNode = document.getElementById('task-field')
    pointsNode.innerHTML = Game.points
    clickNode.innerHTML = Game.click_power
    autoClickNode.innerHTML = Game.auto_click_power
    taskTextNode.innerHTML = Game.task_text
}


function update_boost(boost) {
    const boost_node = document.getElementById(`boost_${boost.id}`)
    boost_node.querySelector('#boost_level').innerText = boost.level
    boost_node.querySelector('#boost_power').innerText = boost.power
    boost_node.querySelector('#boost_price').innerText = boost.price
}


function add_boost(parent, boost) {
    const div = document.createElement('div')
    div.setAttribute('class', 'container-child')
    const button = document.createElement('button')
    button.setAttribute('class', `boost_${boost.type}`)
    button.setAttribute('id', `boost_${boost.id}`)
    button.setAttribute('onclick', `buy_boost(${boost.id})`)
    button.innerHTML = ` 
        <p>lvl: <span id="boost_level">${boost.level}</span></p>
        <p>+<span id="boost_power">${boost.power}</span></p> 
        <p><span id="boost_price">${boost.price}</span></p> 
    `
    div.appendChild(button)
    parent.appendChild(div)
}

function getCore() {
    return fetch('/core/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        return response.core
    }).catch(error => console.log(error))
}


function updatePoints(current_points) {
    const csrftoken = getCookie('csrftoken')
    return fetch('/update_points/', {
        method: 'POST',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            current_points: current_points
        })
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(response => {
        if (response.is_levelup) {
            get_boosts()
        }
        return response.core
    }).catch(error => console.log(error))
}


function get_boosts() {
    return fetch('/boosts/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(boosts => {
        const panel = document.getElementById('boosts-holder')
        panel.innerHTML = ''
        boosts.forEach(boost => {
            add_boost(panel, boost)
        })
    }).catch(error => console.log(error))
}


function buy_boost(boost_id) {
    const csrftoken = getCookie('csrftoken')
    return fetch(`/boost/${boost_id}/`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            points: Game.points
        })
    }).then(response => {
        if (response.ok) return response.json()
        return Promise.reject(response)
    }).then(response => {
        if (response.error) return
        const old_boost_stats = response.old_boost_stats
        const new_boost_stats = response.new_boost_stats

        Game.add_points(-old_boost_stats.price)
        if (old_boost_stats.type === 1) {
            Game.add_auto_power(old_boost_stats.power)
        } else {
            Game.add_power(old_boost_stats.power)
        }
        click_animation(document.getElementById(`boost_${boost_id}`), 200)
        update_boost(new_boost_stats) // Обновляем буст на фронтике.
    }).catch(err => console.log(err))
}


function setAutoClick() {
    setInterval(function () {
        Game.add_points(Game.auto_click_power)
    }, 1000)
}


function setAutoSave() {
    setInterval(function () {
        updatePoints(Game.points)
    }, 60000)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function checkAnswer() {
    const task_field = document.getElementById('task-field')
    const answer_field = document.getElementById('answer-field')
    if (answer_field.value === Game.task_text) {
        answer_field.value = ""
        task_field.style.webkitAnimationName = "rightAnswerAnimation";
        Game.add_points(Game.click_power)
        Game.update_task()
    }
}

window.onload = function () {
    Game.init()
    setAutoClick()
    setAutoSave()
    initAnswerInput()
    initLoadFileForm()
}

function initLoadFileForm() {
    let lang_indicator = document.querySelector("#lang-indicator")
    const form = document.querySelector("#send-form");
    const inputFile = document.querySelector("#input-file");

    inputFile.addEventListener('change', function () {
        let files = this.files;
        if (files.length === 0) {
            return;
        }
        let reader = new FileReader();
        reader.onload = function (event) {
            Game.loaded_words = event.target.result.split(/\r?\n?\s+/);
        };
        reader.readAsText(files[0]);
    })

    form.addEventListener("submit", e => {
        e.preventDefault()
        const csrftoken = getCookie('csrftoken')
        return fetch(`/set_words/`, {
            method: 'PUT',
            headers: {
                "X-CSRFToken": csrftoken,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                lang: "",
                words: Game.loaded_words.join(' ')
            })
        }).then(response => {
            if (response.ok) return response.json()
            return Promise.reject(response)
        }).then(response => {
            if (response.error) return
            Game.words = Game.loaded_words
            lang_indicator.innerText = "мой"
            Game.task_text = generate_task()
        }).catch(err => console.log(err))
    });
}

function initAnswerInput() {
    document.querySelector('#answer-field').oninput = function (event) {
        checkAnswer(event)
    }
    document.querySelector('#task-field').addEventListener('webkitAnimationEnd', function () {
        this.style.webkitAnimationName = "";
    })
}

function switchLang() {
    let lang_indicator = document.querySelector("#lang-indicator")
    const csrftoken = getCookie('csrftoken')
    return fetch(`/switch_lang/`, {
        method: 'PUT',
        headers: {
            "X-CSRFToken": csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({})
    }).then(response => {
        if (response.ok) return response.json()
        return Promise.reject(response)
    }).then(response => {
        if (response.error) return
        Game.words = response.words_set.words.split(/\r?\n?\s+/)
        lang_indicator.innerText = response.words_set.lang
        Game.task_text = generate_task()
    }).catch(err => console.log(err))
}

function click_animation(node, time_ms) {
    css_time = `.0${time_ms}s`
    node.style.cssText = `transition: all ${css_time} linear; transform: scale(0.95);`
    setTimeout(function() {
        node.style.cssText = `transition: all ${css_time} linear; transform: scale(1);`
    }, time_ms)
}
