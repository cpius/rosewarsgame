package com.wotr.cocos.action;

import org.cocos2d.actions.ActionCallback;
import org.cocos2d.nodes.CCNode;

public class ChangeVisibilityNodeCallBackAction implements ActionCallback {

	private final CCNode node;
	private final boolean visible;

	public ChangeVisibilityNodeCallBackAction(CCNode node, boolean visible) {
		this.node = node;
		this.visible = visible;
	}

	@Override
	public void execute() {
		node.setVisible(visible);
	}
}
