package net.wg.infrastructure.base {
    import flash.display.Sprite;
    import net.wg.infrastructure.interfaces.IView;

    /** Compile-time stub for the game's real AbstractView. */
    public class AbstractView extends Sprite implements IView {
        public function AbstractView() {
            super();
        }

        public function get as_config():Object { return null; }
        public function set as_config(value:Object):void { }

        public function get loader():Object { return null; }
        public function set loader(value:Object):void { }

        protected function configUI():void { }
    }
}
