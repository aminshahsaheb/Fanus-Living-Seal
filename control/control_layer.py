cat > control/control_layer.py << 'EOF'
class ControlLayer:
    def decide(self, fi, drift, audit):
        # اولویت اول: اعتماد به نفس پایین
        if audit["confidence"] < 0.5:
            return "HALT"

        # انحراف بحرانی
        if "HIGH_DRIFT" in audit["warnings"]:
            return "REALIGN"

        # انحراف متوسط
        if drift > 0.75:
            return "SLOW_DOWN"

        # چاپلوسی بالا
        if fi > 2:
            return "REDUCE_FLATTERY_RESPONSE"

        # وضعیت عادی
        return "CONTINUE"
EOF
