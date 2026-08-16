package net.wg.infrastructure.interfaces {
    /**
     * Compile-time stub only.
     *
     * The real IView is supplied by the Tanki/Mir Tankov client at runtime.
     * This SWC is passed to mxmlc as an external library and is NOT embedded
     * into WRTracker.swf.
     */
    public interface IView {
        function get as_config():Object;
        function set as_config(value:Object):void;
        function get loader():Object;
        function set loader(value:Object):void;
    }
}
