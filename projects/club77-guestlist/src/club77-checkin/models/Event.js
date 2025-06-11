module.exports = (sequelize, DataTypes) => {
  const Event = sequelize.define('Event', {
    id: {
      type: DataTypes.INTEGER,
      primaryKey: true,
      autoIncrement: true
    },
    name: {
      type: DataTypes.STRING,
      allowNull: false,
      validate: {
        notEmpty: true
      }
    },
    event_date: {
      type: DataTypes.DATEONLY,
      allowNull: false
    },
    // Muzeek integration fields
    muzeek_id: {
      type: DataTypes.STRING,
      allowNull: true,
      unique: true
    },
    description: {
      type: DataTypes.TEXT,
      allowNull: true
    },
    artwork_url: {
      type: DataTypes.STRING,
      allowNull: true
    },
    start_time: {
      type: DataTypes.STRING,
      allowNull: true,
      defaultValue: '10:00 PM'
    },
    end_time: {
      type: DataTypes.STRING,
      allowNull: true,
      defaultValue: '5:00 AM'
    },
    venue: {
      type: DataTypes.STRING,
      allowNull: true,
      defaultValue: '77 William St, Darlinghurst'
    },
    is_live: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: true
    },
    muzeek_published: {
      type: DataTypes.BOOLEAN,
      allowNull: false,
      defaultValue: false
    },
    last_synced: {
      type: DataTypes.DATE,
      allowNull: true
    },
    created_at: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    },
    updated_at: {
      type: DataTypes.DATE,
      defaultValue: DataTypes.NOW
    }
  }, {
    tableName: 'events',
    timestamps: true,
    createdAt: 'created_at',
    updatedAt: 'updated_at'
  });

  Event.associate = function(models) {
    // Event has many Guests
    Event.hasMany(models.Guest, {
      foreignKey: 'event_id',
      as: 'guests',
      onDelete: 'CASCADE'
    });
  };

  return Event;
}; 