import json

expressions = {
    "neutral": {
        "left_eyebrow_outer": 90,
        "left_eyebrow_inner": 90,
        "right_eyebrow_inner": 90,
        "right_eyebrow_outer": 90,
        "eyelid_left": 90,
        "eyelid_right": 90,
        "eye_vertical": 90,
        "eye_horizontal": 90,
        "left_cheek_upper": 90,
        "left_cheek_lower": 90,
        "right_cheek_upper": 90,
        "right_cheek_lower": 90,
        "top_cheek_left": 90,
        "top_cheek_right": 90,
        "top_lip_left": 90,
        "top_lip_center": 90,
        "top_lip_right": 90,
        "bottom_lip_left": 90,
        "bottom_lip_center": 90,
        "bottom_lip_right": 90,
        "mouth": 90
    },
    "happy": {
        "left_eyebrow_inner": 100,
        "right_eyebrow_inner": 100,
        "left_eyebrow_outer": 95,
        "right_eyebrow_outer": 95,
        "eyelid_left": 85,
        "eyelid_right": 85,
        "eye_vertical": 90,
        "eye_horizontal": 90,
        "left_cheek_upper": 120,
        "right_cheek_upper": 120,
        "top_lip_left": 110,
        "top_lip_center": 110,
        "top_lip_right": 110,
        "bottom_lip_left": 130,
        "bottom_lip_center": 130,
        "bottom_lip_right": 130,
        "mouth": 120
    },
    "sad": {
        "left_eyebrow_inner": 60,
        "right_eyebrow_inner": 60,
        "left_eyebrow_outer": 80,
        "right_eyebrow_outer": 80,
        "eyelid_left": 100,
        "eyelid_right": 100,
        "eye_vertical": 92,
        "eye_horizontal": 90,
        "left_cheek_lower": 70,
        "right_cheek_lower": 70,
        "top_lip_left": 75,
        "top_lip_center": 80,
        "top_lip_right": 75,
        "bottom_lip_left": 70,
        "bottom_lip_center": 70,
        "bottom_lip_right": 70,
        "mouth": 60
    }
    # ... more expressions ...
}

def send_expression(expression_name):
    """
    Simulate sending a facial expression to the robot's face display system.
    """
    if expression_name in expressions:
        print(f"Setting expression: {expression_name}")
        # Here you would send the expression to the robot's hardware or UI
        # For now, just print the values
        print(json.dumps(expressions[expression_name], indent=2))
    else:
        print(f"Unknown expression: {expression_name}")
