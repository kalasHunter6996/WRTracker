package wrtracker {
    import flash.display.Sprite;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFormatAlign;
    import net.wg.infrastructure.base.AbstractView;

    public class WrTrackerView extends AbstractView {
        private var panel:Sprite = new Sprite();
        private var accent:Sprite = new Sprite();
        private var progressBg:Sprite = new Sprite();
        private var progressFill:Sprite = new Sprite();
        private var title:TextField = new TextField();
        private var subtitle:TextField = new TextField();
        private var wr:TextField = new TextField();
        private var stats:TextField = new TextField();
        private var targetLabel:TextField = new TextField();
        private var target:TextField = new TextField();
        private var nextLabel:TextField = new TextField();
        private var next:TextField = new TextField();
        private var footer:TextField = new TextField();

        private static const PANEL_W:Number = 430;
        private static const PANEL_H:Number = 154;
        private static const BG:uint = 0x111820;
        private static const PANEL_ALPHA:Number = 0.90;
        private static const ACCENT:uint = 0xF2A900;
        private static const TEXT:uint = 0xE8E8E8;
        private static const MUTED:uint = 0x8F9AA5;

        public function WrTrackerView() {
            super();
            visible = true;
            alpha = 1.0;
            scaleX = 1.0;
            scaleY = 1.0;
            mouseEnabled = false;
            mouseChildren = false;

            panel.graphics.beginFill(BG, PANEL_ALPHA);
            panel.graphics.drawRoundRect(0, 0, PANEL_W, PANEL_H, 10, 10);
            panel.graphics.endFill();
            addChild(panel);

            accent.graphics.beginFill(ACCENT, 1.0);
            accent.graphics.drawRoundRect(0, 0, 4, PANEL_H, 4, 4);
            accent.graphics.endFill();
            addChild(accent);

            setup(title, 18, 10, 220, 20, 15, TEXT, true);
            setup(subtitle, 18, 31, 220, 16, 10, MUTED, false);
            setup(wr, 18, 49, 190, 48, 36, TEXT, true);
            setup(stats, 18, 96, 190, 22, 13, MUTED, false);

            setup(targetLabel, 232, 12, 175, 16, 10, MUTED, false);
            setup(target, 232, 28, 175, 29, 20, TEXT, true);
            setup(nextLabel, 232, 64, 175, 16, 10, MUTED, false);
            setup(next, 232, 80, 175, 29, 20, TEXT, true);
            setup(footer, 18, 128, 389, 18, 10, MUTED, false);

            title.text = "WR TRACKER";
            subtitle.text = "АККАУНТ · СЛУЧАЙНЫЕ БОИ";
            wr.text = "--.--%";
            stats.text = "-- побед · -- боёв";
            targetLabel.text = "СЛЕДУЮЩАЯ ОТМЕТКА";
            target.text = "--";
            nextLabel.text = "СЛЕДУЮЩИЙ ЦЕЛЫЙ %";
            next.text = "--";
            footer.text = "Статистика обновляется в ангаре";

            addChild(title);
            addChild(subtitle);
            addChild(wr);
            addChild(stats);
            addChild(targetLabel);
            addChild(target);
            addChild(nextLabel);
            addChild(next);
            addChild(footer);

            progressBg.graphics.beginFill(0x303942, 1.0);
            progressBg.graphics.drawRoundRect(18, 120, 389, 4, 4, 4);
            progressBg.graphics.endFill();
            addChild(progressBg);

            progressFill.graphics.beginFill(ACCENT, 1.0);
            progressFill.graphics.drawRoundRect(18, 120, 1, 4, 4, 4);
            progressFill.graphics.endFill();
            addChild(progressFill);

            x = 30;
            y = 150;
        }

        private function setup(tf:TextField, px:Number, py:Number, w:Number, h:Number, size:int, color:uint, bold:Boolean):void {
            tf.x = px;
            tf.y = py;
            tf.width = w;
            tf.height = h;
            tf.selectable = false;
            tf.mouseEnabled = false;
            tf.multiline = false;
            tf.wordWrap = false;
            var fmt:TextFormat = new TextFormat();
            fmt.font = "Arial";
            fmt.size = size;
            fmt.color = color;
            fmt.bold = bold;
            fmt.align = TextFormatAlign.LEFT;
            tf.defaultTextFormat = fmt;
            tf.setTextFormat(fmt);
        }

        private function setProgress(current:Number, targetValue:Number):void {
            var start:Number = Math.floor(current);
            if (targetValue <= start) {
                progressFill.width = 389;
                return;
            }
            var ratio:Number = (current - start) / (targetValue - start);
            if (ratio < 0) ratio = 0;
            if (ratio > 1) ratio = 1;
            progressFill.width = Math.max(1, 389 * ratio);
        }

        public function as_setData(wrValue:String, halfTarget:String, halfWins:String, wholeData:String):void {
            if (!wrValue || wrValue == "") {
                return;
            }
            var parts:Array = wholeData.split("|");
            if (parts.length < 4) {
                return;
            }

            var current:Number = Number(wrValue);
            var halfValue:Number = Number(halfTarget);

            wr.text = wrValue + "%";
            stats.text = parts[3] + " побед · " + parts[2] + " боёв";
            target.text = halfTarget + "%  ·  " + halfWins;
            next.text = parts[0] + "%  ·  " + parts[1];
            footer.text = "Побед до цели · данные обновляются автоматически";
            setProgress(current, halfValue);
        }
    }
}
