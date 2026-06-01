def render_metric_card(label, value, unit, description, color=None):
    border = f"border-color:{color}33" if color else ""
    label_style = f"color:{color}" if color else ""
    value_style = f"color:{color}" if color else ""
    return (
        f'<div class="metric-card" style="{border}">'
        f'<div class="metric-label" style="{label_style}">{label}</div>'
        f'<div class="metric-value" style="{value_style}">{value}'
        f'<span class="metric-unit">{unit}</span></div>'
        f'<div class="metric-desc">{description}</div>'
        f'</div>'
    )
