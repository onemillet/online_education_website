/**
 * Created by lixingyu on 2016/10/10.
 */
 KindEditor.ready(function(K) {
                window.editor = K.create('#id_content',{
                    height:'200px',
                    width:'800px',
                    uploadJson: '/admin/upload/kindeditor',
                });
        });