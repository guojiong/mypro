# 入库加库存: 查询库存 1.已有库存,增加库存数量; 2.没有库存,新增库存数据
CREATE TRIGGER trigg_to_store AFTER INSERT ON devops.instore FOR EACH ROW
BEGIN
	IF (SELECT id FROM devops.store WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi AND unit = new.unit) THEN
			UPDATE devops.store
			SET num = (SELECT T.num FROM (SELECT num FROM devops.store WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi AND unit = new.unit) T) + new.num,
			price = ((SELECT N.total FROM (SELECT num*price AS total FROM devops.store WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi AND unit = new.unit) N) + new.num * new.price) / ((SELECT T.num FROM (SELECT num FROM devops.store WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi AND unit = new.unit) T) + new.num)
		WHERE
			project_id = new.project_id
			AND mtype = new.mtype
			AND mclass = new.mclass
			AND mname = new.mname
			AND specifi = new.specifi
			AND unit = new.unit;
	ELSE
		INSERT INTO devops.store SET project_id = new.project_id,
			mtype = new.mtype,
			mclass = new.mclass,
			mname = new.mname,
			specifi = new.specifi,
			num =(SELECT sum( num ) FROM devops.instore WHERE project_id = new.project_id AND mtype = new.mtype AND mclass = new.mclass AND mname = new.mname AND specifi = new.specifi AND unit = new.unit),
			price = new.price,
			unit = new.unit;

	END IF;
END




# 出库减库存
CREATE TRIGGER trigg_out_store AFTER INSERT ON devops.outstore FOR EACH ROW
BEGIN
	UPDATE devops.store 
		SET num = (SELECT tmp.num from (SELECT num FROM devops.store WHERE id = new.store_id) tmp) - new.num 
	WHERE
		id = new.store_id;
END



# 删除采购入库记录,同步库存数量
CREATE TRIGGER del_to_store BEFORE DELETE ON devops.instore FOR EACH ROW
BEGIN
			UPDATE devops.store
			SET num = (SELECT T.num FROM (SELECT num FROM devops.store WHERE id = (SELECT store_id FROM devops.instore WHERE id = old.id)) T) - (SELECT num FROM devops.instore WHERE id = old.id)
			WHERE id = (SELECT store_id FROM devops.instore WHERE id = old.id);
END


# 删除材料出库记录,同步库存数量
CREATE TRIGGER del_outto_store BEFORE DELETE ON devops.outstore FOR EACH ROW
BEGIN
			UPDATE devops.store
			SET num = (SELECT T.num FROM (SELECT num FROM devops.store WHERE id = (SELECT store_id FROM devops.outstore WHERE id = old.id)) T) + (SELECT num FROM devops.outstore WHERE id = old.id)
			WHERE id = (SELECT store_id FROM devops.outstore WHERE id = old.id);
END