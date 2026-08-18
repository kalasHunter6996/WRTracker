package wrtracker {
    import flash.display.Sprite;
    import flash.events.MouseEvent;
    import flash.events.KeyboardEvent;
    import flash.text.TextField;
    import flash.text.TextFormat;
    import flash.text.TextFormatAlign;
    import flash.ui.Keyboard;
    import net.wg.infrastructure.base.AbstractView;

    public class WrTrackerView extends AbstractView {
        private var panel:Sprite = new Sprite();
        private var accent:Sprite = new Sprite();
        private var title:TextField = new TextField();
        private var wr:TextField = new TextField();
        private var target:TextField = new TextField();
        private var next:TextField = new TextField();
        private var hint:TextField = new TextField();
        private var hideButton:TextField = new TextField();
        private var userHidden:Boolean = false;
        private var dragging:Boolean = false;

        private static const PANEL_W:Number = 360;
        private static const PANEL_H:Number = 112;
        private static const BG:uint = 0x111820;
        private static const PANEL_ALPHA:Number = 0.92;
        private static const ACCENT:uint = 0xF2A900;
        private static const TEXT:uint = 0xE8E8E8;
        private static const MUTED:uint = 0x8F9AA5;

        public function WrTrackerView() {
            super();
            visible = true;
            mouseEnabled = true;
            mouseChildren = true;

            panel.graphics.beginFill(BG, PANEL_ALPHA);
            panel.graphics.drawRoundRect(0, 0, PANEL_W, PANEL_H, 9, 9);
            panel.graphics.endFill();
            panel.buttonMode = true;
            panel.addEventListener(MouseEvent.MOUSE_DOWN, onDragStart);
            addChild(panel);

            accent.graphics.beginFill(ACCENT, 1.0);
            accent.graphics.drawRoundRect(0, 0, 3, PANEL_H, 3, 3);
            accent.graphics.endFill();
            addChild(accent);

            setup(title, 14, 9, 230, 18, 13, TEXT, true);
            setup(wr, 14, 27, 150, 40, 30, TEXT, true);
            setup(target, 175, 18, 165, 27, 18, TEXT, true);
            setup(next, 175, 52, 165, 27, 18, TEXT, true);
            setup(hint, 14, 88, 260, 15, 9, MUTED, false);
            setup(hideButton, 327, 8, 22, 20, 14, MUTED, true);

            title.text = "WR TRACKER  ·  АККАУНТ";
            wr.text = "--.--%";
            target.text = "48.0% · --";
            next.text = "49% · --";
            hint.text = "перетащить · F8 — скрыть/показать";
            hideButton.text = "×";
            hideButton.mouseEnabled = true;
            hideButton.addEventListener(MouseEvent.CLICK, onHideClick);

            addChild(title);
            addChild(wr);
            addChild(target);
            addChild(next);
            addChild(hint);
            addChild(hideButton);

            x = 30;
            y = 150;
            if (stage) {
                stage.addEventListener(KeyboardEvent.KEY_DOWN, onKeyDown);
            }
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

        private function onDragStart(event:MouseEvent):void {
            if (event.target == hideButton) return;
            dragging = true;
            startDrag(false);
            stage.addEventListener(MouseEvent.MOUSE_UP, onDragStop);
        }

        private function onDragStop(event:MouseEvent):void {
            if (!dragging) return;
            dragging = false;
            stopDrag();
            stage.removeEventListener(MouseEvent.MOUSE_UP, onDragStop);
        }

        private function onHideClick(event:MouseEvent):void {
            userHidden = true;
            visible = false;
        }

        private function onKeyDown(event:KeyboardEvent):void {
            if (event.keyCode == Keyboard.F8) {
                userHidden = !userHidden;
                visible = !userHidden;
            }
        }

        public function as_isHidden():Boolean {
            return userHidden;
        }

        public function as_show():void {
            userHidden = false;
            visible = true;
        }

        public function as_setData(wrValue:String, halfTarget:String, halfWins:String, wholeData:String):void {
            if (!wrValue || wrValue == "") return;
            var parts:Array = wholeData.split("|");
            if (parts.length < 4) return;

            wr.text = wrValue + "%";
            target.text = halfTarget + "%  ·  " + halfWins;
            next.text = parts[0] + "%  ·  " + parts[1];
        }

        override protected function onDispose():void {
            if (stage) stage.removeEventListener(KeyboardEvent.KEY_DOWN, onKeyDown);
            panel.removeEventListener(MouseEvent.MOUSE_DOWN, onDragStart);
            hideButton.removeEventListener(MouseEvent.CLICK, onHideClick);
            if (stage) stage.removeEventListener(MouseEvent.MOUSE_UP, onDragStop);
            super.onDispose();
        }
    }
}
