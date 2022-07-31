let theme = "";

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function change_css(theme) {
    const container_bg_color = `var(--container-bg-color-${theme})`;
    const body_bg_color = `var(--body-bg-color-${theme})`;
    const text_color = `var(--text-color-${theme})`;
    const border_color = `var(--border-color-${theme})`;
    const transparent_bg_color = `var(--transparent-bg-color-${theme})`;
    const btn_bg_color_hover = `var(--btn-bg-color-hover-${theme})`;
    const btn_text_color_hover = `var(--btn-text-color-hover-${theme})`;
    const shadow_color = `var(--shadow-color-${theme})`;
    const info_text_bg_color = `var(--info-text-bg-color-${theme})`;
    const container_border_color = `var(--container-border-color-${theme})`;
    const btn_text_color = `var(--btn-text-color-${theme})`;
    const alt_text_color = `var(--alt-text-color-${theme})`;
    const svg_img_color = `var(--svg-img-color-${theme})`;

    style = document.body.style;

    style.setProperty("--container-bg-color", container_bg_color);
    style.setProperty("--body-bg-color", body_bg_color);
    style.setProperty("--text-color", text_color);
    style.setProperty("--border-color", border_color);
    style.setProperty("--transparent-bg-color", transparent_bg_color);
    style.setProperty("--btn-bg-color-hover", btn_bg_color_hover);
    style.setProperty("--btn-text-color-hover", btn_text_color_hover);
    style.setProperty("--shadow-color", shadow_color);
    style.setProperty("--info-text-bg-color", info_text_bg_color);
    style.setProperty("--container-border-color", container_border_color);
    style.setProperty("--btn-text-color", btn_text_color);
    style.setProperty("--alt-text-color", alt_text_color);
    style.setProperty("--svg-img-color", svg_img_color);

    const theme_btn = document.getElementById("theme-btn");
    theme_btn.innerHTML = ""
    if (theme === "night") {
        theme_btn.innerHTML = "<svg class=\"navbar-btn_img\" id=\"svg\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"400\" height=\"400\"\n" +
            "     viewBox=\"0, 0, 400,400\">\n" +
            "    <g id=\"svgg\">\n" +
            "        <path\n" +
            "                d=\"M109.375 13.455 C -44.697 92.970,-33.477 326.500,127.304 386.656 C 225.962 423.569,339.241 381.973,383.851 292.453 C 416.015 227.907,405.839 214.274,347.557 243.829 C 220.135 308.446,87.038 175.092,152.679 48.573 C 179.324 -2.784,164.357 -14.921,109.375 13.455 \"\n" +
            "                stroke=\"none\" fill=\"var(--svg-img-color-night)\" fill-rule=\"evenodd\"></path>\n" +
            "    </g>\n" +
            "</svg>"
    } else {
        theme_btn.innerHTML = "<svg class=\"navbar-btn_img\" id=\"svg\" xmlns=\"http://www.w3.org/2000/svg\" xmlns:xlink=\"http://www.w3.org/1999/xlink\" width=\"400\" height=\"400\"\n" +
            "     viewBox=\"0, 0, 400,400\">\n" +
            "    <g id=\"svgg\">\n" +
            "        <path\n" +
            "                d=\"M178.683 28.125 C 171.615 56.286,180.396 75.000,200.678 75.000 C 218.198 75.000,218.750 74.045,218.750 43.750 C 218.750 6.871,187.114 -5.467,178.683 28.125 M66.071 66.071 C 47.754 84.389,71.153 120.778,99.163 117.533 C 123.257 114.741,125.238 87.260,102.627 69.475 C 82.507 53.649,78.836 53.307,66.071 66.071 M297.373 69.475 C 274.762 87.260,276.743 114.741,300.837 117.533 C 312.659 118.903,321.028 114.701,330.525 102.627 C 357.136 68.797,331.203 42.864,297.373 69.475 M153.125 101.044 C 49.529 158.340,84.390 306.250,201.489 306.250 C 309.197 306.250,347.420 169.071,256.740 107.961 C 233.353 92.201,176.032 88.374,153.125 101.044 M12.500 200.000 C 12.500 218.333,13.194 218.750,43.750 218.750 C 74.306 218.750,75.000 218.333,75.000 200.000 C 75.000 181.667,74.306 181.250,43.750 181.250 C 13.194 181.250,12.500 181.667,12.500 200.000 M325.000 200.000 C 325.000 218.333,325.694 218.750,356.250 218.750 C 386.806 218.750,387.500 218.333,387.500 200.000 C 387.500 181.667,386.806 181.250,356.250 181.250 C 325.694 181.250,325.000 181.667,325.000 200.000 M69.475 297.373 C 53.649 317.493,53.307 321.164,66.071 333.929 C 84.389 352.246,120.778 328.847,117.533 300.837 C 114.741 276.743,87.260 274.762,69.475 297.373 M283.811 289.841 C 277.844 305.390,283.449 319.860,300.309 332.435 C 329.168 353.959,353.953 329.208,332.479 300.309 C 318.777 281.870,289.303 275.530,283.811 289.841 M178.683 340.625 C 171.615 368.786,180.396 387.500,200.678 387.500 C 218.198 387.500,218.750 386.545,218.750 356.250 C 218.750 319.371,187.114 307.033,178.683 340.625 \"\n" +
            "                stroke=\"none\" fill=\"var(--svg-img-color-day)\" fill-rule=\"evenodd\"></path>\n" +
            "    </g>\n" +
            "</svg>"
    }
}

function load_current_theme() {
    const csrftoken = getCookie("csrftoken");
    return fetch(`get_theme/`, {
        method: "GET",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (response.ok) return response.json();
            return Promise.reject(response);
        })
        .then((response) => {
            if (response.error) return;
            theme = response.theme;
            change_css(theme);
        })
        .catch((err) => console.log(err));
}

function switch_current_theme() {
    const csrftoken = getCookie("csrftoken");
    return fetch(`/switch_theme/`, {
        method: "PUT",
        headers: {
            "X-CSRFToken": csrftoken,
            "Content-Type": "application/json",
        },
    })
        .then((response) => {
            if (response.ok) return response.json();
            return Promise.reject(response);
        })
        .then((response) => {
            if (response.error) return;
            theme = response.theme;
            change_css(theme);
        })
        .catch((err) => console.log(err));
}

function load_current_lang(){
    return fetch('/get_lang_code/', {
        method: 'GET'
    }).then(response => {
        if (response.ok) {
            return response.json()
        }
        return Promise.reject(response)
    }).then(json_resp => {
        let url_parts = window.location.href.split('/');
        if(url_parts.indexOf(json_resp['lang_code']) == -1){
            let idx = -1;
            for(var i = 0; i < url_parts.length; i++){
                if(url_parts[i].length === 2){
                    idx = i;
                    break;
                }
            }
            url_parts[idx] = json_resp['lang_code']
            window.location.replace(url_parts.join("/"))
        }
    }).catch(error => console.log(error))
}

window.addEventListener("load", function (event) {
    load_current_lang();
    load_current_theme();
});
