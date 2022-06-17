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
      console.log(theme);
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

window.addEventListener("load", function(event) {load_current_theme();});
