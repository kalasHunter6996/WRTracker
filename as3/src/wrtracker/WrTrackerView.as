package wrtracker {
    import flash.display.Sprite;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFormatAlign;
    import net.wg.infrastructure.base.AbstractView;

    public class WrTrackerView extends AbstractView {
        private var bg:Sprite = new Sprite();
        private var title:TextField = new TextField();
        private var wr:TextField = new TextField();
        private var half:TextField = new TextField();
        private var whole:TextField = new TextField();
        private var battles:TextField = new TextField();

        public function WrTrackerView() {
            super();
            visible = true;
            alpha = 1.0;
            scaleX = 1.0;
            scaleY = 1.0;

            bg.graphics.beginFill(0x00FF00, 0.95);
            bg.graphics.drawRect(0, 0, 420, 180);
            bg.graphics.endFill();
            addChild(bg);

            setup(title, 15, 10, 390, 28, 18, 0x000000);
            setup(wr, 15, 40, 390, 40, 30, 0x000000);
            setup(half, 15, 82, 390, 25, 18, 0x000000);
            setup(whole, 15, 110, 390, 25, 18, 0x000000);
            setup(battles, 15, 140, 390, 22, 15, 0x000000);
            title.text = "WR TRACKER TEST";
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
            fmt.font = "Arial";
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
