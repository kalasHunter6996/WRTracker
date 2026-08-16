package wrtracker {
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFormatAlign;
    import net.wg.infrastructure.base.AbstractView;

    // The real client expects Scaleform Views to implement IView. The normal
    // WG base class is AbstractView, which implements IView for us.
    public class WrTrackerView extends AbstractView {
        private var bg:flash.display.Sprite = new flash.display.Sprite();
        private var title:TextField = new TextField();
        private var wr:TextField = new TextField();
        private var half:TextField = new TextField();
        private var whole:TextField = new TextField();
        private var battles:TextField = new TextField();

        public function WrTrackerView() {
            super();

            bg.graphics.beginFill(0x111111, 0.82);
            bg.graphics.drawRoundRect(0, 0, 270, 128, 10, 10);
            bg.graphics.endFill();
            addChild(bg);

            setup(title, 12, 7, 246, 20, 12, 0xBDBDBD);
            setup(wr, 12, 27, 246, 32, 25, 0xFFFFFF);
            setup(half, 12, 60, 246, 20, 14, 0xDADADA);
            setup(whole, 12, 81, 246, 20, 14, 0xDADADA);
            setup(battles, 12, 103, 246, 18, 12, 0xA5A5A5);

            title.text = "WR TRACKER";
            wr.text = "WR TEST";
            half.text = "До .50%: --";
            whole.text = "До следующего %: --";
            battles.text = "Бои: --";
            addChild(title);
            addChild(wr);
            addChild(half);
            addChild(whole);
            addChild(battles);

            x = 30;
            y = 170;
            mouseEnabled = false;
            mouseChildren = false;
        }

        private function setup(tf:TextField, px:Number, py:Number, w:Number, h:Number, size:int, color:uint):void {
            tf.x = px;
            tf.y = py;
            tf.width = w;
            tf.height = h;
            tf.selectable = false;
            tf.mouseEnabled = false;

            var fmt:TextFormat = new TextFormat();
            fmt.font = "$FieldFont";
            fmt.size = size;
            fmt.color = color;
            fmt.align = TextFormatAlign.LEFT;
            tf.defaultTextFormat = fmt;
            tf.setTextFormat(fmt);
        }

        public function as_setData(wrValue:String, halfTarget:String, halfWins:String, wholeData:String):void {
            if (!wrValue || wrValue == "") {
                return;
            }

            var parts:Array = wholeData.split("|");
            if (parts.length < 3) {
                return;
            }

            wr.text = "WR " + wrValue + "%";
            half.text = "До " + halfTarget + "%: " + halfWins + " побед";
            whole.text = "До " + parts[0] + "%: " + parts[1] + " побед";
            battles.text = "Бои: " + parts[2];
        }
    }
}
