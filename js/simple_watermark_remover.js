import { app } from "../../../scripts/app.js";

const HELP_DESCRIPTIONS = [
    { icon: "🖼️", name: "Load Image", zh: "加载图片", desc: "Use a standard Load Image node", zh_desc: "首先使用标准的图片加载节点" },
    { icon: "🖱️", name: "Open Editor", zh: "打开编辑器", desc: "Right-click on the image and select 'Open in MaskEditor'", zh_desc: "在图片上点右键，选择 'Open in MaskEditor'" },
    { icon: "✍️", name: "Draw Mask", zh: "涂抹遮罩", desc: "Paint over the watermark and click 'Save to node'", zh_desc: "涂满水印区域，然后点击右键菜单里的 'Save to node'" },
    { icon: "🔗", name: "Connect", zh: "连接节点", desc: "Connect IMAGE and MASK outputs to this node", zh_desc: "将图片和遮罩两个输出连到本节点" },
    { icon: "🚀", name: "Remove", zh: "去除水印", desc: "Run the prompt and LaMa will do the magic!", zh_desc: "点击运行，LaMa 模型会自动帮你完成修补" }
];

app.registerExtension({
    name: "SimpleWatermarkRemover.Antigravity",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== "SimpleWatermarkRemover") return;

        const proto = nodeType.prototype;
        
        const onNodeCreated = proto.onNodeCreated;
        proto.onNodeCreated = function () {
            onNodeCreated?.apply(this, arguments);
            this.isHoveringHelp = false;
        };

        const onMouseMove = proto.onMouseMove;
        proto.onMouseMove = function (e, pos) {
            const [mx, my] = pos;
            // Detect if mouse is over the "?" icon in the title bar
            const iconArea = [this.size[0] - 25, -LiteGraph.NODE_TITLE_HEIGHT, 25, LiteGraph.NODE_TITLE_HEIGHT];
            const wasHoveringHelp = this.isHoveringHelp;
            this.isHoveringHelp = (mx >= iconArea[0] && mx <= iconArea[0] + iconArea[2] && my >= iconArea[1] && my <= iconArea[1] + iconArea[3]);
            
            if (wasHoveringHelp !== this.isHoveringHelp) {
                this.setDirtyCanvas(true);
            }

            if (this.isHoveringHelp) return true;
            return onMouseMove?.apply(this, arguments);
        };

        proto.onDrawForeground = function (ctx) {
            // Draw the "?" icon in the title bar
            const iconX = this.size[0] - 22, iconY = -LiteGraph.NODE_TITLE_HEIGHT + 5, iconR = 8;
            ctx.save();
            ctx.fillStyle = this.isHoveringHelp ? "#fff" : "#ff0";
            ctx.font = "bold 15px Arial";
            ctx.textAlign = "center";
            ctx.textBaseline = "middle";
            ctx.fillText("?", iconX + iconR, iconY + iconR);

            if (this.isHoveringHelp) {
                this._drawHelpSidebar(ctx);
            }
            ctx.restore();
        };

        proto._drawHelpSidebar = function (ctx) {
            const margin = 15;
            const bx = this.size[0] + 15;
            const labelFont = "bold 13px Arial";
            const descFont = "normal 11px Arial";
            const itemHeight = 40;

            ctx.save();
            ctx.textBaseline = "middle";

            // 1. Calculate dimensions
            let maxLabelW = 0;
            let maxDescW = 0;
            ctx.font = labelFont;
            HELP_DESCRIPTIONS.forEach(item => {
                maxLabelW = Math.max(maxLabelW, ctx.measureText(`${item.zh} / ${item.name}`).width);
                ctx.font = descFont;
                maxDescW = Math.max(maxDescW, ctx.measureText(`- ${item.zh_desc} / ${item.desc}`).width);
                ctx.font = labelFont;
            });

            const labelX = bx + margin + 28;
            const descX = labelX + maxLabelW + 15;
            const boxW = (descX - bx) + maxDescW + margin;
            const boxH = HELP_DESCRIPTIONS.length * itemHeight + 50;
            const by = -LiteGraph.NODE_TITLE_HEIGHT;

            // 2. Draw Background Box
            ctx.fillStyle = "rgba(10, 10, 10, 0.98)";
            ctx.strokeStyle = "#ff0";
            ctx.lineWidth = 2;
            if (ctx.roundRect) {
                ctx.beginPath();
                ctx.roundRect(bx, by, boxW, boxH, 12);
                ctx.fill();
                ctx.stroke();
            } else {
                ctx.fillRect(bx, by, boxW, boxH);
                ctx.strokeRect(bx, by, boxW, boxH);
            }

            // 3. Draw Header
            ctx.font = "bold 16px Arial";
            ctx.textAlign = "left";
            ctx.fillStyle = "#ff0";
            ctx.fillText("如何使用 / How to use", bx + margin, by + 25);

            // 4. Draw Items
            HELP_DESCRIPTIONS.forEach((item, i) => {
                const y = by + 60 + i * itemHeight;
                ctx.font = "18px Arial";
                ctx.fillStyle = "#fff";
                ctx.fillText(item.icon, bx + margin, y);
                
                ctx.font = labelFont;
                ctx.fillStyle = "#fff";
                ctx.fillText(`${item.zh} / ${item.name}`, labelX, y - 8);
                
                ctx.font = descFont;
                ctx.fillStyle = "#aaa";
                ctx.fillText(`- ${item.zh_desc} / ${item.desc}`, labelX, y + 10);
            });
            ctx.restore();
        };
    }
});
