package com.wotr.cocos.action;

import org.cocos2d.actions.ActionCallback;
import org.cocos2d.layers.CCLayer;
import org.cocos2d.nodes.CCNode;

public class RemoveNodeCalBackAction implements ActionCallback {

	private final CCLayer layer;
	private final CCNode node;

	public RemoveNodeCalBackAction(CCLayer layer, CCNode node) {
		this.layer = layer;
		this.node = node;
	}

	@Override
	public void execute() {
		node.removeAllChildren(true);
		layer.removeChild(node, true);
	}

}
